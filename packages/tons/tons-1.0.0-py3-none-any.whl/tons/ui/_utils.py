import dataclasses
import os
from datetime import datetime
from enum import Enum
from typing import Optional, Iterable, Tuple, List, Dict
from xmlrpc.client import Boolean

import requests
from dateutil.relativedelta import relativedelta
from prettytable import MARKDOWN, PrettyTable

from tons import settings
from tons.config import init_config, Config, TonProviderEnum
from tons.tonclient import TonClient, DAppTonClient
from tons.tonclient._client._base import NftItemInfoResult, TonDaemon, AddressInfoResult
from tons.tonclient._client._dapp._daemon import DAppBroadcastDaemon
from tons.tonclient.utils import KeyStores, GlobalWhitelist, BaseKeyStore, Record, WhitelistContact
from tons.tonsdk.utils import from_nano, TonCurrencyEnum, Address
from tons.tonsdk.utils.tonconnect.requests_responses import SendTransactionRequest, AppRequestMethodEnum
from tons.utils import storage
from tons.utils.versioning import tons_is_outdated


@dataclasses.dataclass
class SharedObject:
    config: Config
    ton_client: TonClient
    ton_daemon: TonDaemon
    specific_config_path: Optional[str]
    background_task_manager: Optional["BackgroundTaskManager"] = None  # noqa: F821
    keystores: Optional[KeyStores] = None
    keystore: Optional[BaseKeyStore] = None
    whitelist: Optional[GlobalWhitelist] = None
    debug_mode: Boolean = False
    extra: Optional[Dict] = None


class TxAction(str, Enum):
    confirm = "Confirm"
    cancel = "Cancel"


def init_shared_object(specific_config_path: str = None) -> SharedObject:
    config = init_config(specific_config_path)
    ton_client = get_ton_client(config)
    ton_daemon = get_ton_daemon(config, ton_client)

    return SharedObject(
        config=config, specific_config_path=specific_config_path, ton_client=ton_client, ton_daemon=ton_daemon)


def setup_app(config: Config):
    if config.tons.warn_if_outdated and tons_is_outdated():
        print("\033[93mWarning: tons version is outdated! "
              "Please, see the update guide: https://tonfactory.github.io/tons-docs/installation#update\033[0m")

    for default_dir_path in [config.tons.workdir,
                             config.tons.keystores_path]:
        try:
            storage.ensure_dir_exists(default_dir_path)
        except PermissionError as e:
            raise PermissionError(f'Workdir "{e.filename}" inaccessible or unmounted.')


def get_ton_client(config: Config):
    if config.tons.provider == TonProviderEnum.dapp:
        return DAppTonClient(config)
    else:
        raise NotImplementedError


def get_ton_daemon(config: Config, client: TonClient) -> TonDaemon:
    if config.tons.provider == TonProviderEnum.dapp:
        assert isinstance(client, DAppTonClient)
        return DAppBroadcastDaemon(config, client)
    else:
        raise NotImplementedError


def pin_is_valid(pin: str):
    if len(pin) != 6:
        return False

    return True


class CustomPrettyTable(PrettyTable):
    def get_string(self, **kwargs):
        self.align["Name"] = 'l'
        self.align["Comment"] = 'l'
        self.align["Balance"] = 'r'

        return super().get_string()


def md_table() -> CustomPrettyTable:
    table = CustomPrettyTable()
    table.set_style(MARKDOWN)
    return table


def form_wallets_table(wallets_info: Tuple[Record],
                       verbose: bool,
                       wallets_verbose_info: Optional[List[AddressInfoResult]] = None,
                       total_required: bool = False):
    # wallet list, whitelist list
    field_names = ['Name', 'Version', 'WC', 'Address', 'Comment']
    if verbose:
        field_names += ['State', 'Balance']

    table = md_table()
    table.field_names = field_names
    if verbose:
        total = 0
        for wallet, wallet_info in zip(wallets_info, wallets_verbose_info):
            total += wallet_info.balance
            table.add_row([wallet.name, wallet.version, wallet.workchain,
                           wallet.address_to_show, wallet.comment,
                           wallet_info.state.value, format(wallet_info.balance, 'f')])
        if wallets_info and total_required:
            table.add_row(["Total", "", "", "", "", "", format(total, 'f')])
    else:
        for wallet in wallets_info:
            table.add_row([wallet.name, wallet.version, wallet.workchain,
                           wallet.address_to_show, wallet.comment])

    return table


def form_tonconnect_table(connections):
    table = md_table()
    table.field_names = ["Wallet", "Connected at", "Dapp Name", "Dapp Url", "Dapp Client Id"]
    for connection in connections:
        table.add_row([connection.wallet_name, connection.connected_datetime,
                       connection.app_manifest.name, connection.app_manifest.url, connection.dapp_client_id])

    return table


def form_whitelist_table(contacts: Tuple[WhitelistContact],
                         verbose: bool,
                         contact_infos: Optional[List[AddressInfoResult]] = None,
                         title: Optional[str] = None):
    field_names = ["Contact name", "Address", "Message"]
    if verbose:
        field_names += ['State', 'Balance']

    table = md_table()
    if title:
        table.title = title
    table.field_names = field_names
    table.align["Contact name"] = 'l'
    table.align["Message"] = 'l'
    if verbose:
        for contact, contact_info in zip(contacts, contact_infos):
            table.add_row([contact.name, contact.address_to_show, contact.default_message,
                           contact_info.state.value, format(contact_info.balance, 'f')])

    else:
        for contact in contacts:
            table.add_row([contact.name, contact.address_to_show, contact.default_message])

    return table


def form_dns_table(dns_items_info: Iterable[NftItemInfoResult], display_not_owned=True) -> CustomPrettyTable:
    """
    Form a DNS table based on the provided DNS item information.

    Args:
        dns_items_info (Iterable[NftItemInfoResult]): Iterable containing DNS item information.
        display_not_owned (bool, optional): Determines whether to display items that are not owned
        but have won auctions. Defaults to True.

    Returns:
        CustomPrettyTable: A formatted table containing DNS domain information.

    Note:
        The table includes the following fields:
        - "DNS domain": The domain name for the DNS item.
        - "Last fill-up time": The timestamp of the last fill-up time (GMT).
        - "Expires in": The remaining time in days until the item's expiration.

        If `display_not_owned` is True, the table will also include the following field:
        - "Status": The status of the DNS item, indicating whether it is owned or won in an auction.

        The field "Owner" will be renamed to "Owner / max bidder" if `display_not_owned` is True.
    """
    field_names = ["DNS domain", "Last fill-up time", "Expires in"]
    if display_not_owned:
        field_names.append("Owner / max bidder")
        field_names.append("Status")
    else:
        field_names.append("Owner")
    table = md_table()
    table.field_names = field_names

    for dns_item in dns_items_info:
        if not display_not_owned and not dns_item.owner_address:
            continue
        dns_domain = dns_item.dns_domain + '.ton'
        last_fill_up_time = str(datetime.utcfromtimestamp(dns_item.dns_last_fill_up_time)) + ' GMT'
        expires_in = f"{(datetime.utcfromtimestamp(dns_item.dns_expires) - datetime.now()).days} days"
        status = 'owned' if dns_item.owner_address else 'auction won'
        row = [dns_domain, last_fill_up_time, expires_in, dns_item.owner_or_max_bidder]
        if display_not_owned:
            row.append(status)

        table.add_row(row)

    return table


def form_request_info(req: SendTransactionRequest):
    if req.method == AppRequestMethodEnum.send_transaction:
        params_info = []
        for i, param in enumerate(req.params):
            messages_str = "\n".join(
                [
                    f"* Send {from_nano(int(message.amount), TonCurrencyEnum.ton)} TON "
                    f"to {Address(message.address).to_string(True)}"
                    for message in
                    param.messages])

            valid_until = ""
            if param.valid_until is not None:
                valid_until = f"valid until {datetime.fromtimestamp(int(param.valid_until) / 10 ** 3)}, "
            params_info.append(f"Operation {i + 1} ({valid_until}"
                               f"request to send {len(param.messages)} messages)\n{messages_str}")

        return "\n".join(params_info)

    else:
        raise NotImplementedError(f"Request with the method '{req.method}' is not implemented.")


def dns_expires_soon(dns_item: NftItemInfoResult, months_max_expiring_in: int) -> bool:
    return datetime.utcfromtimestamp(dns_item.dns_expires) < datetime.now() + \
        relativedelta(months=months_max_expiring_in)


def shorten_dns_domain(domain):
    if len(domain) > 25:
        domain = domain[:11] + '...' + domain[-11:]
    return domain


def split_into_lines(text: str, line_max_length: int = 48):
    return '\n'.join(text[i:i + line_max_length] for i in range(0, len(text), line_max_length))


def truncate(text: str, max_len: int = 100):
    if len(text) > max_len:
        return text[:max_len - 3] + '...'
    return text


def fetch_known_jettons():
    """
    Fetches a list of known jettons from https://github.com/tonkeeper/ton-assets
    :raises: requests.RequestException, requests.JSONDecodeError
    :return: parsed json of known jetton addresses
    """
    response = requests.get(settings.KNOWN_JETTONS_URL)
    response.raise_for_status()
    return response.json()


def fetch_known_jettons_addresses() -> Tuple[Address]:
    """
    Fetches a list of known jettons from https://github.com/tonkeeper/ton-assets
    Returns:
        Tuple[Address]: A tuple containing the list of known jetton addresses.
        If the fetch fails, an empty tuple is returned.
    """
    try:
        return tuple(Address(jetton['address']) for jetton in fetch_known_jettons())
    except (requests.RequestException, requests.JSONDecodeError):
        return tuple()


def getcwd_pretty():
    return os.getcwd().replace(os.sep, "/")
