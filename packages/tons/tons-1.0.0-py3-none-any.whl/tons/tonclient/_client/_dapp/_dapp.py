import asyncio
import decimal
from datetime import datetime
from threading import Lock
from time import sleep
from typing import List, Union, Optional, Tuple, Dict

from tons import settings
from tons.config import Config
from tons.tonsdk.boc import Cell
from tons.tonsdk.contract.token.ft import JettonWallet
from tons.tonsdk.contract.wallet import SendModeEnum, WalletContract, InternalMessage
from tons.tonsdk.provider.dapp import DAppClient, DAppWrongResult, BroadcastQuery
from tons.tonsdk.utils import TonCurrencyEnum, from_nano, Address, b64str_to_bytes, \
    bytes_to_b64str, to_nano
from ._queries import Accounts, Comparison, DAppGqlQuery, NftItems, JettonWallets, JettonMinters, raw_ids
from .._base import TonClient, AddressInfoResult, BroadcastResult, BroadcastStatusEnum, NftItemInfoResult, \
    JettonWalletResult, JettonMinterResult, AddressState
from ..._exceptions import TonDappError, TON_EXCEPTION_BY_CODE


class InsufficientBalanceError(TonDappError):
    pass


class DAppTonClient(TonClient):
    TRY_AGAIN_SLEEP_SEC = 5

    def __init__(self, config: Config):
        self.config = config
        self._provider: DAppClient = None
        self.lock = Lock()

    @property
    def provider(self):
        if self._provider is None:
            self._provider = DAppClient(graphql_url=self.config.provider.dapp.graphql_url,
                                        broadcast_url=self.config.provider.dapp.broadcast_url,
                                        websocket_url=self.config.provider.dapp.websocket_url,
                                        api_key=self.config.provider.dapp.api_key,
                                        network=self.config.provider.dapp.network)

        return self._provider

    def get_address_information(self, address: str,
                                currency_to_show: TonCurrencyEnum = TonCurrencyEnum.ton) -> Optional[AddressInfoResult]:
        return self.get_addresses_information([address], currency_to_show)[0]

    def get_addresses_information(self, addresses: List[str],
                                  currency_to_show: TonCurrencyEnum = TonCurrencyEnum.ton) -> \
            List[Optional[AddressInfoResult]]:
        if not addresses:
            return []

        address_ids = raw_ids(addresses)
        queries = [Accounts.by_ids(address_ids[i:i + settings.DAPP_RECORDS_LIMIT]).gql()
                   for i in range(0, len(address_ids), settings.DAPP_RECORDS_LIMIT)]
        results = self._run(self.provider.query(queries), single_query=False)
        accounts = []
        for result in results:
            accounts += result['accounts']

        address_infos = [None] * len(address_ids)
        for account in accounts:
            for idx, address_id in enumerate(address_ids):
                if address_id == account['id']:
                    address_infos[idx] = self._parse_addr_info(account, currency_to_show)
        for i in range(len(address_infos)):
            if address_infos[i] is None:
                address_infos[i] = AddressInfoResult(address=addresses[i], state=AddressState.uninit, balance=0)

        return address_infos

    def get_dns_items_information(self, holders: List[Union[Address, str]], include_max_bid: bool = True) \
            -> List[NftItemInfoResult]:
        """
        Retrieve DNS items information for the specified holders.

        Args:
            holders (List[Union[Address, str]]): A list of holders (addresses or address strings)
                to retrieve DNS items information for.
            include_max_bid (bool, optional): Determines whether to include DNS items where the holders
                are the maximum bidders in finished auctions, but did not claim ownership. Defaults to True.

        Returns:
            List[NftItemInfoResult]: A list of NftItemInfoResult objects containing DNS items information.

        Note:
            - The function retrieves DNS items information for the specified holders.
            - If `include_max_bid` is True, DNS items where the holders are the maximum bidders in finished auctions,
              but have not yet claimed their ownership, will also be included in the returned list.
            - The function uses pagination to retrieve the results in batches.
            - If no holders are provided, an empty list is returned.
        """
        if not holders:
            return []
        result = []

        query = NftItems.DNS(self.config.provider.dapp.dns_collection_address)
        query.filter.add(Comparison.owner_address_in(holders))
        result += [NftItemInfoResult(**r) for r in self._paginate(query)]

        if include_max_bid:
            query = NftItems.DNS(self.config.provider.dapp.dns_collection_address)
            query.filter.add(Comparison.dns_max_bidder_in(holders))
            query.filter.add(Comparison.dns_auction_finished())
            result += [NftItemInfoResult(**r) for r in self._paginate(query)]

        return result

    def get_dns_domain_information(self, dns_domain: str, raise_none: bool = True) -> Optional[NftItemInfoResult]:
        query = NftItems.DNS(self.config.provider.dapp.dns_collection_address)
        query.filter.add(Comparison.dns_domain(dns_domain), behavior='replace')
        result = self._run_gql_query(query)
        try:
            result = result[0]
        except IndexError:
            if raise_none:
                raise TonDappError(f"Failed to retrieve dns info: {dns_domain}.ton")
            return None

        return NftItemInfoResult(**result)

    def get_jetton_information(self, owners: List[Union[Address, str]]) \
            -> Tuple[List[JettonMinterResult], List[JettonWalletResult]]:
        if not owners:
            return [], []

        wallets_query = JettonWallets()
        wallets_query.filter.add(Comparison.owner_address_in(owners))
        jetton_wallets = [JettonWalletResult(**r) for r in self._paginate(wallets_query)]

        if len(jetton_wallets) == 0:
            return [], []

        minters_query = JettonMinters()
        minters_query.filter.add(Comparison.address_in([item.jetton_master_address for item in jetton_wallets]))
        jetton_minters = [JettonMinterResult(**r) for r in self._paginate(minters_query)]

        return jetton_minters, jetton_wallets

    def get_jetton_wallet(self, owner: Union[Address, str], minter_address: Union[Address, str],
                          raise_none: bool = True) -> Optional[JettonWalletResult]:
        query = JettonWallets()
        query.filter.add(Comparison.owner_address(owner))
        query.filter.add(Comparison.jetton_master_address(minter_address))
        result = self._run_gql_query(query)
        try:
            result = result[0]
        except IndexError:
            if raise_none:
                raise TonDappError(f"Failed to retrieve jetton wallet info: owner={owner} minter={minter_address}")
            return None

        return JettonWalletResult(**result)

    def _paginate(self, query: DAppGqlQuery):
        previous_last_id = None
        while True:
            query.add_pagination(previous_last_id)
            query_result = self._run_gql_query(query)
            yield from query_result
            try:
                previous_last_id = query_result[-1]['id']
            except IndexError:
                break

    def seqno(self, addr: str) -> int:
        return self.get_address_information(addr).seqno

    def deploy_wallet(self, wallet: WalletContract, wait_for_result=False):
        timeout = 30 if wait_for_result else 0
        query = wallet.create_init_external_message()
        base64_boc = bytes_to_b64str(query["message"].to_boc(False))
        result = self._run(self.provider.broadcast(
            [BroadcastQuery(boc=base64_boc, timeout=timeout)]))

        return query, self._parse_broadcast_result(result, wait_for_result)

    def transfer(self, from_wallet: WalletContract, messages: List[InternalMessage], wait_for_result=False,
                 attempts=2) -> [Dict, BroadcastResult]:
        """
        Transfer ton from the specified `from_wallet` to the provided list of recipients using internal messages.

        Args:
            from_wallet (WalletContract): The wallet contract from which the funds will be transferred.
            messages (List[InternalMessage]): A list of `InternalMessage` objects representing the transfer details.
            wait_for_result (bool, optional): Determines whether to wait for the transfer result.
                Defaults to False.
            attempts (int, optional): Retry attempts times in case the transfer fails with `exitcode=33`.
                Before retrying, sleep for TRY_AGAIN_SLEEP_SEC seconds, to let the backend update the seqno.
                Defaults to True.

        Returns:
            [Dict, BroadcastResult]: A tuple containing the transfer query and the broadcast result.

        Raises:
            InsufficientBalanceError: If the `from_wallet` does not have sufficient balance to cover the total amount
            of the transfer.

        Note:
            The `wait_for_result` parameter affects the timeout duration for waiting for the transfer result.
            The timeout is set to 30 seconds if `wait_for_result` is True, or 0 seconds if `wait_for_result` is False.
        """
        timeout = 30 if wait_for_result else 0

        addresses = [message.to_addr.to_string() for message in messages] + [from_wallet.address.to_string()]
        addresses_info = self.get_addresses_information(addresses, currency_to_show=TonCurrencyEnum.nanoton)
        from_address_info: AddressInfoResult = addresses_info.pop()

        total_amount = sum([to_nano(message.amount, src_unit=message.currency) for message in messages])
        if total_amount > from_address_info.balance:
            raise InsufficientBalanceError("Insufficient balance")

        for idx, message in enumerate(messages):
            if addresses_info[idx].state in (AddressState.uninit, AddressState.non_exist):
                message.to_addr.is_bounceable = False

        query = from_wallet.create_transfer_message(seqno=from_address_info.seqno, messages=messages)
        msg_boc = query["message"].to_boc(False)
        base64_boc = bytes_to_b64str(msg_boc)
        try:
            result = self._run(self.provider.broadcast([BroadcastQuery(boc=base64_boc, timeout=timeout)]))
        except TonDappError as dapp_error:
            # TODO:
            #  Fix this, the exitcode should not be parsed from verbose details.
            #  Best solution would be to implement returning exitcode as part of the response from the backend.
            if attempts > 0 and "exitcode=33" in dapp_error.detail:
                sleep(DAppTonClient.TRY_AGAIN_SLEEP_SEC)
                return self.transfer(from_wallet, messages, wait_for_result, attempts=attempts - 1)
            raise dapp_error
        return query, self._parse_broadcast_result(result, wait_for_result)

    def refresh_dns_ownership(self, from_wallet: WalletContract,
                              dns_item: NftItemInfoResult,
                              wait_for_result: bool = False):
        if dns_item.owner_address:
            amount = self.config.dns.refresh_send_amount
            payload = ""
        else:
            amount = self.config.dns.refresh_not_yet_owned_send_amount
            payload = Cell()
            op_change_dns_record = 0x4eb1f0f9
            query_id = 0
            mock_dict_key = 0
            payload.bits.write_uint(op_change_dns_record, 32)
            payload.bits.write_uint(query_id, 64)
            payload.bits.write_uint(mock_dict_key, 256)

        messages = [InternalMessage(
            to_addr=Address(dns_item.account.address),
            amount=amount,
            currency=TonCurrencyEnum.ton,
            body=payload,
        )]

        return self.transfer(from_wallet, messages=messages, wait_for_result=wait_for_result)

    def jetton_transfer(self, from_wallet: WalletContract, from_jetton_wallet_addr: Address,
                        to_address: Union[str, Address], jetton_amount: int, gas_amount: decimal.Decimal,
                        wait_for_result: bool = False):
        jetton_transfer_body = JettonWallet().create_transfer_body(to_address=to_address,
                                                                   jetton_amount=jetton_amount,
                                                                   forward_amount=0,
                                                                   forward_payload=None,
                                                                   response_address=from_wallet.address,
                                                                   query_id=0)

        messages = [InternalMessage(
            send_mode=SendModeEnum.ignore_errors,
            to_addr=from_jetton_wallet_addr,
            amount=gas_amount,
            currency=TonCurrencyEnum.ton,
            body=jetton_transfer_body,
        )]

        return self.transfer(from_wallet=from_wallet, messages=messages, wait_for_result=wait_for_result)

    def send_boc(self, boc: bytes, wait_for_result: bool):
        timeout = 30 if wait_for_result else 0
        base64_boc = bytes_to_b64str(boc)
        result = self._run(self.provider.broadcast(
            [BroadcastQuery(boc=base64_boc, timeout=timeout)]))

        return self._parse_broadcast_result(result, wait_for_result)

    def _run(self, to_run, *, single_query=True):
        with self.lock:
            try:
                results = asyncio.get_event_loop().run_until_complete(to_run)
            except DAppWrongResult as e:
                if len(e.errors) == 1 and e.errors[0].code in TON_EXCEPTION_BY_CODE:
                    raise TON_EXCEPTION_BY_CODE[e.errors[0].code]

                raise TonDappError(str(e))

            except Exception as e:  # ClientConnectorError, ...?
                exception_text = str(e)
                if not exception_text:
                    exception_text = repr(e)

                raise TonDappError(exception_text)

            if single_query:
                return results[0]

            return results

    def _run_gql_query(self, query: DAppGqlQuery):
        return self._run(self.provider.query([query.gql()]))[query.name]

    def _parse_addr_info(self, result: dict, currency_to_show: TonCurrencyEnum = TonCurrencyEnum.ton):
        return AddressInfoResult(
            address=result['address'],
            # contract_type='wallet v3r2',  # FIXME
            seqno=self._get_seqno(result),
            state=result['acc_type_name'],
            balance=self._get_balance(result, currency_to_show),
            last_activity=self._get_last_paid(result),
            code=result['code'],
            data=result['data'],
        )

    @staticmethod
    def _get_seqno(result: dict):
        if result['acc_type_name'] in [AddressState.active, AddressState.frozen]:
            # TODO: check contract type and version
            data_cell = Cell.one_from_boc(b64str_to_bytes(result["data"]))
            if len(data_cell.bits) > 32:
                seqno = 0
                for bit in data_cell.bits[:32]:
                    seqno = (seqno << 1) | bit
                return seqno

        return 0

    @staticmethod
    def _get_balance(result: dict, currency_to_show: TonCurrencyEnum) -> decimal.Decimal:
        if "balance" in result and result["balance"]:
            if int(result["balance"]) < 0:
                balance = 0
            else:
                balance = from_nano(int(result["balance"]), currency_to_show)
        else:
            balance = 0

        return decimal.Decimal(balance)

    @staticmethod
    def _get_last_paid(result: dict):
        if "last_paid" in result and result["last_paid"]:
            return str(datetime.utcfromtimestamp(
                result['last_paid']).strftime('%Y-%m-%d %H:%M:%S'))

    @staticmethod
    def _parse_broadcast_result(result, waited) -> BroadcastResult:
        if "status" in result:
            if result["status"] == 1 and waited:
                status = BroadcastStatusEnum.committed
            else:
                status = BroadcastStatusEnum.broadcasted
        else:
            status = BroadcastStatusEnum.failed

        return BroadcastResult(waited=waited, status=status)
