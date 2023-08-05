import asyncio
import decimal
import sys
import uuid
from queue import SimpleQueue
from threading import Thread
from typing import Union, Dict, List

from tons.config import Config
from tons.tonclient import DAppTonClient
from tons.tonclient._client._base import BroadcastResult, TonDaemon, TonDaemonResult, DaemonTask, DaemonTaskNameEnum, \
    NftItemInfoResult, TonDaemonGoodbye
from tons.tonclient._exceptions import TonDappError
from tons.tonsdk.contract.wallet import WalletContract, InternalMessage
from tons.tonsdk.utils import Address


class DAppBroadcastDaemon(TonDaemon):
    def __init__(self, config: Config, client: DAppTonClient):
        self._results_queue: SimpleQueue[Union[TonDaemonResult, TonDaemonGoodbye]] = SimpleQueue()
        self.config = config
        self._client = client
        self._is_running = False
        self._thread = None
        self._tasks_queue: SimpleQueue[DaemonTask] = SimpleQueue()

    def start(self):
        if self._thread is not None:
            raise RuntimeError('Broadcast daemon thread already exists.')

        self._is_running = True
        self._thread = Thread(target=self._run_background_tasks, daemon=True, name='DApp Daemon')
        self._thread.start()

    def stop(self):
        """
        Stop the daemon, but wait until it finishes the current task.
        """
        if self._thread is None:
            raise RuntimeError('Broadcast daemon thread does not exist.')

        self._is_running = False
        self._tasks_queue.put(DaemonTask(task_name=DaemonTaskNameEnum.stop, kwargs=dict()))
        while self._thread.is_alive():
            ...
        self._thread = None

    def transfer(self, from_wallet: WalletContract, messages: List[InternalMessage]) -> uuid.UUID:
        return self._add_task(DaemonTaskNameEnum.transfer, locals())

    def refresh_dns_ownership(self, from_wallet: WalletContract, dns_item: NftItemInfoResult):
        return self._add_task(DaemonTaskNameEnum.refresh_dns, locals())

    def jetton_transfer(self, from_wallet: WalletContract, from_jetton_wallet_addr: Address,
                        to_address: Address, jetton_amount: int, gas_amount: decimal.Decimal):
        return self._add_task(DaemonTaskNameEnum.jetton_transfer, locals())

    def deploy_wallet(self, wallet: WalletContract) -> uuid.UUID:
        return self._add_task(DaemonTaskNameEnum.deploy_wallet, locals())

    def _add_task(self, task_name: DaemonTaskNameEnum, kwargs: Dict) -> uuid.UUID:
        kwargs = {k: v for k, v in kwargs.items() if k != 'self'}
        if not kwargs.get('wait_for_result', True):
            raise RuntimeError("wait_for_result must be set to True for tasks running inside Broadcast Daemon")
        kwargs['wait_for_result'] = True
        task = DaemonTask(task_name=task_name, kwargs=kwargs)
        self._tasks_queue.put(task)
        return task.task_id

    def _run_background_tasks(self):
        # Crutch to fix bug specific to Python 3.8
        # https://stackoverflow.com/questions/60359157/valueerror-set-wakeup-fd-only-works-in-main-thread-on-windows-on-python-3-8-wit
        if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        while self._is_running:
            task = self._tasks_queue.get()
            if task.task_name == DaemonTaskNameEnum.stop:
                self._is_running = False
                break
            task_result = self._perform_task(task)
            self._results_queue.put(TonDaemonResult(task_id=task.task_id, broadcast_result=task_result))

        self._results_queue.put(TonDaemonGoodbye())
        loop.close()

    def _perform_task(self, task: DaemonTask) -> Union[BroadcastResult, TonDappError]:
        methods_map = {DaemonTaskNameEnum.transfer: self._client.transfer,
                       DaemonTaskNameEnum.jetton_transfer: self._client.jetton_transfer,
                       DaemonTaskNameEnum.deploy_wallet: self._client.deploy_wallet,
                       DaemonTaskNameEnum.refresh_dns: self._client.refresh_dns_ownership}
        try:
            try:
                method = methods_map[task.task_name]
            except KeyError:
                raise NotImplementedError(f"{task.task_name} not supported")
            else:
                _, result = method(**task.kwargs)
                return result
        except TonDappError as e:
            return e

    @property
    def results_queue(self) -> SimpleQueue:
        assert self._thread.is_alive()
        return self._results_queue


def _exclude_self(params: Dict):
    return {k: v for k, v in params.items() if k != 'self'}
