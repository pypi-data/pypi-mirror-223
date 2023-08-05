from collections import OrderedDict
from datetime import datetime
from typing import Dict, Tuple, Sequence
from typing import Optional
from typing import OrderedDict as OrderedDictTyping
from uuid import UUID

from colorama import Fore

from tons.tonclient._client._base import NftItemInfoResult
from tons.tonsdk.contract.wallet import Wallets
from tons.tonsdk.utils import InvalidAddressError, Address
from ._base import BaseSet, MenuItem
from ._mixin import KeyStoreMixin, keystore_sensitive_area
from .._modified_inquirer import terminal, ListWithFilter, ModifiedConfirm
from .._utils import echo_success, echo_error, processing
from ..._background import BackgroundTask
from ..._utils import SharedObject, form_dns_table, dns_expires_soon, shorten_dns_domain


class DNSSet(BaseSet, KeyStoreMixin):
    def __init__(self, ctx: SharedObject) -> None:
        super().__init__(ctx)
        self._menu_message = f"Pick DNS command [{self.ctx.keystore.name}]"

    def _handlers(self) -> OrderedDictTyping[str, MenuItem]:
        ord_dict = OrderedDict()
        ord_dict[f"{terminal.underline}R{terminal.no_underline}efresh ownership"] = \
            MenuItem(self._handle_refresh_ownership, "r")
        ord_dict[f"{terminal.underline}L{terminal.no_underline}ist DNS"] = \
            MenuItem(self._handle_show_dns, "l")
        ord_dict[f"{terminal.underline}B{terminal.no_underline}ack"] = \
            MenuItem(self._handle_exit, "b")
        return ord_dict

    def _handle_refresh_ownership(self) -> None:
        with processing():
            addresses = [record.address for record in self.ctx.keystore.get_records(self.ctx.config.tons.sort_keystore)]
            dns_items_info = self.ctx.ton_client.get_dns_items_information(addresses)

        if len(dns_items_info) == 0:
            echo_success("You do not have any domains.", only_msg=True)
            return

        choices = ['(all expiring sooner than in %d months)' % self.ctx.config.dns.max_expiring_in] + \
                  [self.__menufy_dns_info(item) for item in dns_items_info]
        values = [None] + dns_items_info

        questions = [
            ListWithFilter(
                "domain",
                message="Select domain to refresh",
                choices=ListWithFilter.zip_choices_and_values(choices, values),
                carousel=True
            ),
            ModifiedConfirm(
                "wait_for_result", message="Wait until transaction will be completed?", default=True),
        ]
        ans = self._prompt(questions)
        if ans['domain'] is None:
            items_to_refresh = [item for item in dns_items_info
                                if dns_expires_soon(item, self.ctx.config.dns.max_expiring_in)]
        else:
            items_to_refresh = [ans['domain']]

        self._refresh_ownership(items_to_refresh, ans["wait_for_result"])

    def _handle_show_dns(self):
        with processing():
            addresses = [record.address for record in self.ctx.keystore.get_records(self.ctx.config.tons.sort_keystore)]
            dns_items_info = self.ctx.ton_client.get_dns_items_information(addresses)
        echo_success(str(form_dns_table(dns_items_info)), only_msg=True)

    def __menufy_dns_info(self, dns_item) -> str:
        dns_domain = shorten_dns_domain(dns_item.dns_domain) + '.ton'
        try:
            mask = Address(dns_item.account.address).to_mask()
        except InvalidAddressError:
            mask = 'NA'
        try:
            expires_datetime = datetime.utcfromtimestamp(int(dns_item.dns_expires))
        except TypeError:
            expires = 'NA'
        else:
            expires = expires_datetime.strftime('%Y-%m-%d %H:%M:%S')
            if dns_expires_soon(dns_item, self.ctx.config.dns.max_expiring_in):
                expires = Fore.RED + expires + Fore.RESET

        return '{:<30} [{}  expires: {} GMT]'.format(dns_domain, mask, expires)

    def _refresh_ownership(self, dns_items: Sequence[NftItemInfoResult], wait_for_result: bool):
        if len(dns_items) == 0:
            echo_success('No domain needs to update ownership.')
            return
        self.__refresh_ownership(dns_items, wait_for_result)

    @keystore_sensitive_area
    def __refresh_ownership(self, dns_items: Sequence[NftItemInfoResult], wait_for_result: bool):
        pending_tasks: Dict[UUID, NftItemInfoResult] = {}

        for dns_item in dns_items:
            try:
                record = self.ctx.keystore.get_record_by_address(Address(dns_item.owner_or_max_bidder))
            except InvalidAddressError:
                echo_error(f"{shorten_dns_domain(dns_item.dns_domain)}.ton: Invalid NFT data.")
                continue
            with processing():
                mnemonics = self.ctx.keystore.get_secret(record).split(" ")
                _, _, _, wallet = Wallets.from_mnemonics(mnemonics,
                                                         record.version, record.workchain, record.subwallet_id)
                task_id = self.ctx.background_task_manager.dns_refresh_task(from_wallet=wallet, dns_item_info=dns_item)
                pending_tasks[task_id] = dns_item

        if not wait_for_result:
            echo_success("Transactions have been queued.")
            return

        while len(pending_tasks) > 0:
            with processing():
                task_id, dns_item, task = self.__get_next_finished_task(pending_tasks)
            _echo = echo_success if not task.result_is_bad else lambda msg: echo_error(msg, only_cross=True)
            _echo(f"{shorten_dns_domain(dns_item.dns_domain)}.ton: {task.result_description}. "
                 f"Wallet address: {dns_item.owner_or_max_bidder}")
            del pending_tasks[task_id]

    def __get_next_finished_task(self, pending_tasks: Dict[UUID, NftItemInfoResult]) -> \
            Optional[Tuple[UUID, NftItemInfoResult, BackgroundTask]]:
        while True:
            for task_id, dns_item in pending_tasks.items():
                if not (task := self.ctx.background_task_manager.get_task(task_id)).is_pending:
                    return task_id, dns_item, task
