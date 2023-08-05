import base64
import decimal
import uuid
from abc import ABC, abstractmethod
from enum import Enum
from hashlib import sha256
from queue import SimpleQueue
from typing import List, Optional, Union, Tuple, Dict

import requests
from pydantic import BaseModel, root_validator, Field, validator

from tons.config import Config
from tons.tonclient._exceptions import TonError
from tons.tonsdk.boc import Cell, Slice
from tons.tonsdk.contract.wallet import WalletContract, InternalMessage
from tons.tonsdk.utils import TonCurrencyEnum, Address


class NftItemType(int, Enum):
    nft_item = 0
    nft_item_editable = 1
    dns_item = 2
    fragment_item = 3

    def __str__(self) -> str:
        return super().__str__()


class AddressState(str, Enum):
    uninit = 'Uninit'
    active = 'Active'
    frozen = 'Frozen'
    non_exist = 'NonExist'


class AddressInfoResult(BaseModel):
    address: Optional[str] = None
    contract_type: Optional[str] = None
    seqno: Optional[Union[int, str]] = None
    state: Optional[AddressState] = None
    balance: Optional[decimal.Decimal] = None
    last_activity: Optional[str] = None
    code: Optional[str] = None
    data: Optional[str] = None

    data_cell: Optional[Cell] = None

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True

    @validator('seqno')
    def __validate_seqno(cls, v) -> int:
        if v is None:
            return 0
        return int(v)

    @root_validator(pre=False)
    def __parse_data_to_boc(cls, values):
        if not values['data']:
            return values
        values['data_cell'] = Cell.one_from_boc(base64.b64decode(values['data']))
        return values

    @property
    def version(self) -> Optional[int]:
        """
        Guess the wallet version based on its data size.

        Returns:
            Optional[int]: Guessed wallet version based on the data size (2, 3 or 4). Does not include the revision.
                Returns None if the wallet version is unknown or unsupported.
        """
        if not self.data:
            return
        if len(self.data_cell.bits) == 288:
            return 2
        elif len(self.data_cell.bits) == 320:
            return 3
        elif len(self.data_cell.bits) > 320:
            return 4

    @property
    def public_key(self) -> Optional[bytes]:
        """
        Get public key associated with the wallet.

        Returns:
            Optional[bytes]: Public key if available, None otherwise.
        """
        if not self.data:
            return

        if self.version <= 2:
            sc = Slice(self.data_cell)
            sc.read_uint(32)  # skip seqno
            return sc.read_bytes(256 // 8)

        if self.version in (3, 4):
            sc = Slice(self.data_cell)
            sc.read_uint(32)  # skip seqno
            sc.read_uint(32)  # skip subwallet_id
            return sc.read_bytes(256 // 8)

    @property
    def can_receive_encrypted_payload(self):
        return self.public_key is not None


class BroadcastStatusEnum(str, Enum):
    broadcasted = "broadcasted"
    committed = "committed"
    failed = "failed"


class BroadcastResult(BaseModel):
    waited: bool
    status: BroadcastStatusEnum

    class Config:
        use_enum_values = True
        validate_assignment = True

    def __str__(self):
        if self.status == BroadcastStatusEnum.committed:
            return "Transaction has been committed."

        if self.status == BroadcastStatusEnum.broadcasted:
            if self.waited:
                return "Transaction has been sent but hasn't been committed into blockchain during 30 seconds."
            else:
                return "Transaction has been sent."

        return "Transaction hasn't been sent."


class DNSAuction(BaseModel):
    auction_end_time: Optional[int] = None
    max_bid_amount: Optional[int] = None
    max_bid_address: Optional[str] = None


class NftItemInfoResult(BaseModel):
    nft_item_type: Optional[NftItemType] = None
    owner_address: Optional[str] = None
    dns_domain: Optional[str] = None
    dns_last_fill_up_time: Optional[int] = None
    account: Optional[AddressInfoResult] = None
    dns_auction: Optional[DNSAuction] = None

    @property
    def dns_expires(self) -> Optional[int]:
        if self.dns_last_fill_up_time is None:
            return None

        # https://github.com/ton-blockchain/dns-contract/blob/d08131031fb659d2826cccc417ddd9b98476f814/func/dns-utils.fc#LL2C19-L2C19  # noqa: E501
        return self.dns_last_fill_up_time + 31622400

    @property
    def owner_or_max_bidder(self) -> Optional[str]:
        try:
            return self.owner_address or self.dns_auction.max_bid_address
        except AttributeError:
            return None


class ContentTypeEnum(str, Enum):
    Onchain = 'Onchain'
    Offchain = 'Offchain'

    def __str__(self) -> str:
        return super().__str__()


class JettonWalletResult(BaseModel):
    balance: Optional[int] = None
    jetton_master_address: Optional[str] = None
    jetton_wallet_code_hash: Optional[str] = None
    owner_address: Optional[str] = None
    last_trans_lt: Optional[int] = None
    account: Optional[AddressInfoResult] = None

    def balance_readable(self, metadata: 'JettonMetadata') -> decimal.Decimal:
        return jetton_amount_to_readable(self.balance, metadata)


class JettonMinterContent(BaseModel):
    content_type: Optional[int] = None
    content_type_name: Optional[ContentTypeEnum] = None
    data: Optional[List] = None
    uri: Optional[str] = None


class JettonMetadata(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    symbol: Optional[str] = None
    decimals: Union[str, int] = 9
    image_data: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def __cached_sha256(key, memo=dict()):
        if key not in memo:
            memo[key] = sha256(key.encode('utf-8')).hexdigest()
        return memo[key]

    @validator('decimals')
    def __validate_decimals(cls, value):
        try:
            return int(value)
        except ValueError:
            return 9

    @classmethod
    def from_content(cls, content: JettonMinterContent):
        fields = dict()
        try:
            content_data = {item['key']: item['value'] for item in content.data}
        except (KeyError, TypeError):
            pass
        else:
            for fld in ('name', 'description', 'symbol', 'decimals', 'image_data', 'uri'):
                try:
                    fields[fld] = content_data[cls.__cached_sha256(fld)]
                except KeyError:
                    pass

        try:
            fields['uri'] = cls.__ipfs_to_https(fields['uri'])
        except (KeyError, AttributeError):
            pass

        try:
            content.uri = cls.__ipfs_to_https(content.uri)
        except AttributeError:
            pass

        try:
            result = requests.get(fields['uri'])
        except Exception:
            try:
                result = requests.get(content.uri)
            except Exception:
                pass

        try:
            json_dict = result.json()
        except Exception:
            pass
        else:
            for fld, val in json_dict.items():
                fields[fld] = val

        return cls(**fields)

    @staticmethod
    def __ipfs_to_https(uri: str) -> str:
        if uri.startswith('ipfs://'):
            return uri.replace('ipfs://', 'https://ipfs.io/ipfs/')
        return uri


class JettonMinterResult(BaseModel):
    jetton_wallet_code_hash: Optional[str] = None
    admin_address: Optional[str] = None
    last_trans_lt: Optional[int] = None
    account: Optional[AddressInfoResult] = None
    content: Optional[JettonMinterContent] = None

    metadata: Optional[JettonMetadata] = None

    @root_validator(pre=False)
    def __add_metadata(cls, values):
        values['metadata'] = JettonMetadata.from_content(values['content'])
        del values['content']
        return values


def jetton_amount_to_readable(amount: int, metadata: JettonMetadata) -> decimal.Decimal:
    return decimal.Decimal(amount) / decimal.Decimal(10 ** metadata.decimals)


def jetton_amount_from_readable(amount_readable: decimal.Decimal, metadata: JettonMetadata) -> int:
    return int(amount_readable * 10 ** metadata.decimals)


class TonClient(ABC):
    @abstractmethod
    def __init__(self, config: Config):
        raise NotImplementedError

    @abstractmethod
    def get_address_information(self, address: str,
                                currency_to_show: TonCurrencyEnum = TonCurrencyEnum.ton) -> AddressInfoResult:
        raise NotImplementedError

    @abstractmethod
    def get_addresses_information(self, addresses: List[str],
                                  currency_to_show: TonCurrencyEnum = TonCurrencyEnum.ton) -> List[AddressInfoResult]:
        raise NotImplementedError

    @abstractmethod
    def get_dns_items_information(self, holders: List[Union[Address, str]], include_max_bid: bool = True) -> \
            List[NftItemInfoResult]:
        raise NotImplementedError

    @abstractmethod
    def get_dns_domain_information(self, dns_domain: str) -> Optional[NftItemInfoResult]:
        raise NotImplementedError

    @abstractmethod
    def get_jetton_information(self, owners: List[Union[Address, str]]) \
            -> Tuple[List[JettonMinterResult], List[JettonWalletResult]]:
        raise NotImplementedError

    @abstractmethod
    def get_jetton_wallet(self, owner: Union[Address, str], minter_address: Union[Address, str],
                          raise_none: bool = False) -> JettonWalletResult:
        raise NotImplementedError

    @abstractmethod
    def seqno(self, addr: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def deploy_wallet(self, wallet: WalletContract, wait_for_result=False) -> BroadcastResult:
        raise NotImplementedError

    @abstractmethod
    def transfer(self, from_wallet: WalletContract, messages: List[InternalMessage],
                 wait_for_result=False) -> [Dict, BroadcastResult]:
        raise NotImplementedError

    @abstractmethod
    def refresh_dns_ownership(self, from_wallet: WalletContract, dns_item: NftItemInfoResult,
                              wait_for_result: bool = False):
        raise NotImplementedError

    @abstractmethod
    def jetton_transfer(self, from_wallet: WalletContract, from_jetton_wallet_addr: Address,
                        to_address: Union[str, Address], jetton_amount: int, gas_amount: decimal.Decimal,
                        wait_for_result: bool = False):
        raise NotImplementedError

    @abstractmethod
    def send_boc(self, boc: bytes, wait_for_result: bool) -> BroadcastResult:
        raise NotImplementedError


# ======================================================================================================================

class DaemonTaskNameEnum(str, Enum):
    transfer = 'transfer'
    jetton_transfer = 'jetton_transfer'
    deploy_wallet = 'deploy_wallet'
    refresh_dns = 'refresh_dns'

    stop = 'stop'


class DaemonTask(BaseModel):
    task_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    task_name: DaemonTaskNameEnum
    kwargs: Dict

    class Config:
        arbitrary_types_allowed = True

    def __str__(self):
        return f"id:{self.task_id}"


class TonDaemonResult(BaseModel):
    task_id: uuid.UUID
    broadcast_result: Union[BroadcastResult, TonError]

    class Config:
        arbitrary_types_allowed = True

    def __str__(self):
        return f'id:{self.task_id} broadcast:{self.broadcast_result}'


class TonDaemonGoodbye:
    pass


class TonDaemon(ABC):
    @abstractmethod
    def __init__(self, config: Config, client: TonClient):
        raise NotImplementedError

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    @abstractmethod
    def transfer(self, from_wallet: WalletContract, messages: List[InternalMessage]) -> uuid.UUID:
        raise NotImplementedError

    @abstractmethod
    def refresh_dns_ownership(self, from_wallet: WalletContract, dns_item: NftItemInfoResult):
        raise NotImplementedError

    @abstractmethod
    def jetton_transfer(self, from_wallet: WalletContract, from_jetton_wallet_addr: Address,
                        to_address: Address, jetton_amount: int,
                        gas_amount: decimal.Decimal) -> uuid.UUID:
        raise NotImplementedError

    @abstractmethod
    def deploy_wallet(self, wallet: WalletContract) -> uuid.UUID:
        raise NotImplementedError

    @property
    @abstractmethod
    def results_queue(self) -> SimpleQueue:
        raise NotImplementedError
