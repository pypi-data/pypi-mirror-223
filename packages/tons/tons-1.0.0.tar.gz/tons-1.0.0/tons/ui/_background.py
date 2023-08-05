import asyncio
import decimal
from copy import deepcopy
from datetime import datetime
from enum import Enum
from threading import Thread, Lock
from typing import Union, Dict, Optional, List
from uuid import UUID

from colorama import Fore
from pydantic import BaseModel, Field

from tons.tonclient._client._base import TonDaemonResult, BroadcastResult, BroadcastStatusEnum, \
    NftItemInfoResult, JettonMinterResult, jetton_amount_to_readable, AddressInfoResult, AddressState, \
    TonDaemonGoodbye
from tons.tonclient._exceptions import TonError, TonDappError
from tons.tonsdk.contract.wallet import WalletContract, SendModeEnum, InternalMessage
from tons.tonsdk.utils import Address, TonCurrencyEnum
from tons.ui._utils import shorten_dns_domain, SharedObject


class BackgroundTaskError(TonDappError):
    pass


class BackgroundTaskEnum(str, Enum):
    transfer = 'transfer'
    dns_refresh = 'dns_refresh'
    jetton_transfer = 'jetton_transfer'


class BackgroundTask(BaseModel):
    is_pending: bool = True
    result: Optional[TonDaemonResult] = None
    result_description: str = ''
    result_is_bad: bool = False
    time_start: datetime = Field(default_factory=datetime.now)
    time_finish: Optional[datetime] = None

    @property
    def description(self):
        raise NotImplementedError

    def set_result_bad(self):
        self.result_is_bad = True
        if self.result_description.startswith(Fore.RED):
            return
        self.result_description = Fore.RED + self.result_description + Fore.RESET


class TransferBackgroundTask(BackgroundTask):
    amount: decimal.Decimal
    src_addr: Address
    dst_addr: Address
    transfer_all: bool

    class Config:
        arbitrary_types_allowed = True

    @property
    def description(self) -> str:
        if self.transfer_all:
            _amount = 'all remaining coins'
        else:
            _amount = f'{self.amount} TON'
        return f'Transfer {_amount} from {self.src_addr.to_mask()} to {self.dst_addr.to_mask()}'


class DNSRefreshBackgroundTask(BackgroundTask):
    dns_item_info: NftItemInfoResult

    @property
    def description(self) -> str:
        return f'Refresh {shorten_dns_domain(self.dns_item_info.dns_domain)}.ton'


class JettonTransferBackgroundTask(BackgroundTask):
    symbol: str
    amount_readable: decimal.Decimal
    src_addr: Address
    dst_addr: Address

    class Config:
        arbitrary_types_allowed = True

    @property
    def description(self):
        return f'Transfer ' \
               f'{self.amount_readable} ' \
               f'{self.symbol if self.symbol else "UNKNOWN"} ' \
               f'from {self.src_addr.to_mask()} ' \
               f'to {self.dst_addr.to_mask()}'


class DeployWalletBackgroundTask(BackgroundTask):
    wallet_addr: Address

    class Config:
        arbitrary_types_allowed = True

    @property
    def description(self):
        return f'Init wallet {self.wallet_addr.to_mask()}'


class BackgroundTaskManager:
    def __init__(self, ctx: SharedObject):
        self.ctx = ctx

        self._tasks: Dict[UUID, BackgroundTask] = dict()
        self._thread = None

        self._tasks_access_lock = Lock()

    def transfer_task(self, from_wallet: WalletContract, to_addr: str,
                      amount: Union[int, str, decimal.Decimal], payload=None,
                      send_mode=SendModeEnum.ignore_errors | SendModeEnum.pay_gas_separately,
                      state_init=None) -> UUID:
        with self._tasks_access_lock:
            messages = [InternalMessage(
                to_addr=Address(to_addr),
                amount=amount,
                send_mode=send_mode,
                body=payload,
                currency=TonCurrencyEnum.ton,
                state_init=state_init,
            )]
            task_id = self.ctx.ton_daemon.transfer(from_wallet, messages)
            self._tasks[task_id] = TransferBackgroundTask(amount=amount,
                                                          transfer_all=bool(send_mode &
                                                                            SendModeEnum.carry_all_remaining_balance),
                                                          src_addr=from_wallet.address, dst_addr=Address(to_addr))
        return task_id

    def dns_refresh_task(self, from_wallet: WalletContract, dns_item_info: NftItemInfoResult) -> UUID:
        with self._tasks_access_lock:
            task_id = self.ctx.ton_daemon.refresh_dns_ownership(from_wallet, dns_item_info)
            self._tasks[task_id] = DNSRefreshBackgroundTask(dns_item_info=dns_item_info)
        return task_id

    def jetton_transfer_task(self, jetton_minter_info: JettonMinterResult, from_wallet: WalletContract,
                             from_jetton_wallet_addr: Address, to_address: Address,
                             jetton_amount: int, gas_amount: decimal.Decimal) \
            -> UUID:

        with self._tasks_access_lock:
            task_id = self.ctx.ton_daemon.jetton_transfer(from_wallet, from_jetton_wallet_addr, to_address,
                                                          jetton_amount,
                                                          gas_amount)
            self._tasks[task_id] = JettonTransferBackgroundTask(
                amount_readable=jetton_amount_to_readable(jetton_amount, jetton_minter_info.metadata),
                symbol=jetton_minter_info.metadata.symbol or '',
                src_addr=from_wallet.address,
                dst_addr=to_address
            )
        return task_id

    def deploy_wallet_task(self, wallet: WalletContract) -> UUID:
        with self._tasks_access_lock:
            task_id = self.ctx.ton_daemon.deploy_wallet(wallet)
            self._tasks[task_id] = DeployWalletBackgroundTask(wallet_addr=Address(wallet.address))
        return task_id

    def start(self):
        if self._thread is not None:
            while self._thread.is_alive():
                ...
        # The thread runs until it receives a goodbye message from the broadcast daemon
        self._thread = Thread(target=self._run, daemon=True, name="Background task manager")
        self._thread.start()

    @property
    def tasks_list(self) -> List[BackgroundTask]:
        with self._tasks_access_lock:
            return sorted([deepcopy(task) for task in self._tasks.values()], key=lambda t: t.time_start)

    @property
    def tasks_list_empty(self) -> bool:
        return len(self._tasks) == 0

    def get_task(self, task_id: UUID) -> BackgroundTask:
        with self._tasks_access_lock:
            return deepcopy(self._tasks[task_id])

    def _run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        while True:
            r = self.ctx.ton_daemon.results_queue.get()
            if isinstance(r, TonDaemonGoodbye):
                break
            elif isinstance(r, TonDaemonResult):
                pass
            else:
                raise TypeError(f"Unexpected result from TON daemon: {r}")

            with self._tasks_access_lock:
                self._tasks[r.task_id].is_pending = False
                self._tasks[r.task_id].time_finish = datetime.now()
                self._tasks[r.task_id].result = r
                self.finalize(self._tasks[r.task_id])

    @property
    def unfinished_tasks_remaining(self):
        with self._tasks_access_lock:
            return any([t.is_pending for t in self._tasks.values()])

    def finalize(self, task: BackgroundTask):
        if task.result is not None:
            if not isinstance(task.result.broadcast_result, BroadcastResult):
                task.result_description = f'{task.result.broadcast_result}'
                task.set_result_bad()
                return

            bcr = task.result.broadcast_result
            task.result_description = f'{bcr.status}'

            if bcr.status == BroadcastStatusEnum.failed:
                task.set_result_bad()

            if isinstance(task, DNSRefreshBackgroundTask):
                if bcr.status != BroadcastStatusEnum.failed:
                    try:
                        updated_dns_info: NftItemInfoResult = \
                            self.ctx.ton_client.get_dns_domain_information(task.dns_item_info.dns_domain)
                    except TonError as e:
                        task.result_description = f"{bcr.status} but failed to check refreshment: " + str(e)
                        task.set_result_bad()
                    else:
                        if updated_dns_info.dns_last_fill_up_time > task.dns_item_info.dns_last_fill_up_time:
                            task.result_description = \
                                f"refreshed (expires " \
                                f"{datetime.utcfromtimestamp(updated_dns_info.dns_expires)} GMT)"
                        else:
                            task.result_description = f"ownership update {bcr.status} but failed to verify success, " \
                                                      f"please check the domain status manually"
                            task.set_result_bad()

            if isinstance(task, DeployWalletBackgroundTask):
                if bcr.status != BroadcastStatusEnum.failed:
                    try:
                        updated_address_info: AddressInfoResult = \
                            self.ctx.ton_client.get_address_information(task.wallet_addr)
                    except TonError as e:
                        task.result_description = \
                            f"{bcr.status} but failed to verify: " + str(e)
                        task.set_result_bad()
                    else:
                        if updated_address_info.state == AddressState.active:
                            task.result_description = 'wallet initialized'
                        else:
                            task.result_description = 'failed to init wallet'
                            task.set_result_bad()
