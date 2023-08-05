import dataclasses
import os
from abc import ABC
from base64 import b64encode
from copy import deepcopy
from enum import Enum
from typing import List, Optional, Union, Tuple

from tons.tonclient.utils import RecordDoesNotExistError, RecordAlreadyExistsError
from tons.tonclient.utils._exceptions import RecordNameInvalidError, InvalidMnemonicsError
from tons.tonclient.utils._keystores._record import Record
from tons.tonclient.utils._tonconnect import TonconnectConnection, Tonconnector
from tons.tonclient.utils._whitelist import WhitelistContact, LocalWhitelist
from tons.tonsdk.contract.wallet import WalletVersionEnum, Wallets
from tons.tonsdk.crypto.exceptions import InvalidMnemonicsError as sdk_InvalidMnemonicsError
from tons.tonsdk.utils import Address


class KeyStoreTypeEnum(str, Enum):
    password = "password"
    yubikey = "yubikey"

    def __str__(self):
        return self.value


@dataclasses.dataclass
class KeyStoreUpgradeInfo:
    has_been_upgraded: bool = False
    backup_path: Optional[str] = None
    old_version: Optional[int] = None


class BaseKeyStore(ABC):
    def __init__(self, filepath: str, version: int, keystore_type: KeyStoreTypeEnum,
                 records: Union[List[Record], bytes], contacts: Union[List[WhitelistContact], bytes],
                 connections: Union[List[TonconnectConnection], bytes]):
        self.filepath = filepath
        self.name = os.path.basename(filepath)
        self.type = keystore_type
        self.version = version
        self.crypto = {}
        self._records = records
        self.contacts = contacts
        self.connections = connections
        self._whitelist = None
        self._tonconnector = None
        self.upgrade_info = KeyStoreUpgradeInfo()

    @property
    def has_been_upgraded(self) -> bool:
        """
        Informs if the keystore has been upgraded to the next version and backed up
        """
        return self.upgrade_info.has_been_upgraded

    def set_upgraded(self, backup_path: str, old_version: int):
        """
        Marks the keystore as upgraded and sets the backup path and old version
        """
        self.upgrade_info.has_been_upgraded = True
        self.upgrade_info.backup_path = backup_path
        self.upgrade_info.old_version = old_version

    def get_records(self, sort_records: bool) -> Tuple[Record]:
        if sort_records:
            return tuple(sorted(self._records, key=lambda record: record.name.lower()))
        return tuple(self._records)

    @classmethod
    def new(cls, **kwargs) -> 'BaseKeyStore':
        """
        generate new keystore
        """
        raise NotImplementedError

    @classmethod
    def load(cls, json_data) -> 'BaseKeyStore':
        """
        load keystore from file and upgrade to the latest version if required
        """
        raise NotImplementedError

    def save(self, records_before: Optional[List[Record]] = None,
             contacts_before: Optional[List[WhitelistContact]] = None,
             connections_before: Optional[List[TonconnectConnection]] = None):
        """
        save encoded data to self.filepath file or restore state with records_before in case of an error
        """
        try:
            self._save()
        except Exception:
            if records_before is not None:
                self._records = records_before
            if contacts_before is not None:
                self.whitelist._contacts = contacts_before
            if connections_before is not None:
                self.tonconnector.connections = connections_before
            raise

    def _save(self):
        raise NotImplementedError

    def unlock(self, **kwargs):
        """
        decode non sensitive records data (e.g. address)
        """
        raise NotImplementedError

    def get_secret(self, record: Record) -> str:
        """
        get mnemonic from the record
        """
        raise NotImplementedError

    def _create_record_secret_key(self, mnemonics: List[str]):
        """
        encode mnemonics
        """
        raise NotImplementedError

    def encrypt_secret(self, secret: bytes) -> bytes:
        """
        encode secret
        """
        raise NotImplementedError

    def decrypt_secret(self, encrypted_secret: bytes) -> bytes:
        """
        decode secret
        """
        raise NotImplementedError

    @property
    def whitelist(self) -> LocalWhitelist:
        """
        local whitelist
        """
        raise NotImplementedError

    @property
    def tonconnector(self) -> Tonconnector:
        """
        tonconnector handles tonconnect connections in a keystore
        """
        raise NotImplementedError

    def get_record_by_name(self, name: str, raise_none: bool = False) -> Optional[Record]:
        return self._get_record(name=name, raise_none=raise_none)

    def get_record_by_address(self, address: Union[str, Address], raise_none: bool = False) -> Optional[Record]:
        return self._get_record(address=address, raise_none=raise_none)

    def add_new_record(self, name: str,
                       mnemonics: List[str], version: WalletVersionEnum,
                       workchain: int, subwallet_id: Optional[int] = None,
                       comment: Optional[str] = None, save=False, allow_empty_name=False):

        sk = self._create_record_secret_key(mnemonics)
        if not name and not allow_empty_name:
            raise RecordNameInvalidError('Record name should not be empty.')

        try:
            _, _, _, wallet = Wallets.from_mnemonics(mnemonics, version, workchain, subwallet_id)
        except sdk_InvalidMnemonicsError as exc:
            raise InvalidMnemonicsError(f'Invalid mnemonics: {mnemonics}') from exc

        record = Record(name=name, address=wallet.address, version=version, workchain=workchain,
                        subwallet_id=subwallet_id, comment=comment,
                        secret_key=b64encode(sk).decode("utf-8"))

        if self._get_record(name=record.name, address=record.address) is not None:
            address = record.address
            if isinstance(record.address, Address):
                address = record.address.to_string(True, True, True)
            raise RecordAlreadyExistsError(
                f"Record with the name '{record.name}' "
                f"or address: '{address}' already exists")

        records_before = self._records
        self._records.append(record)

        if save:
            self.save(records_before)

    def edit_record(self, name: str, new_name: str, new_comment: str, save: bool = False):
        record = self.get_record_by_name(name, raise_none=True)
        records_before = deepcopy(self._records)
        connections_before = deepcopy(self.tonconnector.connections)
        record_idx = self._records.index(record)
        if new_name:
            if new_name != name and self.get_record_by_name(new_name, raise_none=False) is not None:
                raise RecordAlreadyExistsError(
                    f"Record with the name '{new_name}' already exists")

            self._records[record_idx].name = new_name
            self.tonconnector.update_wallet_name(name, new_name, save=False)
        if new_comment:
            self._records[record_idx].comment = new_comment

        if save:
            self.save(records_before=records_before, connections_before=connections_before)

    def delete_record(self, name: str, save: bool = False) -> Record:
        record = self.get_record_by_name(name, raise_none=True)
        if save:
            records_before = deepcopy(self._records)
            connections_before = deepcopy(self.tonconnector.connections)
            self.tonconnector.delete_all_by_name(name, save=False)
            self._records.remove(record)
            self.save(records_before=records_before, connections_before=connections_before)
        else:
            self.tonconnector.delete_all_by_name(name, save=False)
            self._records.remove(record)

        return record

    def _get_record(self, name: Optional[str] = None, address: Union[str, Address, None] = None,
                    raise_none: bool = False) -> Optional[Record]:
        record = None

        if name is not None:
            record = next(
                (record for record in self._records if record.name == name), record)
            if record is None and raise_none:
                raise RecordDoesNotExistError(
                    f"Record with the name {name} does not exist")

        if address is not None:
            address = address if isinstance(
                address, str) else address.to_string(False, False, False)
            record = next(
                (record for record in self._records if record.address == address), record)
            if record is None and raise_none:
                raise RecordDoesNotExistError(
                    f"Record with the address {address} does not exist")

        if name is None and address is None and raise_none:
            raise RecordDoesNotExistError("Record with the name/address None does not exist")

        return record

    def pretty_string(self):
        icon = ""
        if self.type == KeyStoreTypeEnum.password:
            icon = "🔒"
        elif self.type == KeyStoreTypeEnum.yubikey:
            icon = "🔐"

        return f"{icon} {os.path.basename(self.filepath)}"
