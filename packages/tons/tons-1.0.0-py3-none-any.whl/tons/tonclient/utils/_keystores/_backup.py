from typing import Optional, Union, List, Dict

from pydantic import BaseModel

from tons import settings
from tons.tonsdk.contract.wallet import WalletVersionEnum, WalletContract
from tons.tonsdk.utils import Address
from ._keystore import BaseKeyStore
from ._record import Record
from .._whitelist import WhitelistContact


class TonCliRecordBackup(BaseModel):
    name: str
    comment: Optional[str] = ""
    config: str
    kind: str
    address: Union[str, Address]
    mnemonics: List[str]

    class Config:
        use_enum_values = True
        validate_assignment = True
        arbitrary_types_allowed = True

    def to_backup_record(self) -> Optional["RecordBackup"]:
        if not self.__supported_wallet():
            return None

        version = self.__map_kind_to_version()
        workchain = int(self.__map_config_to_workchain())

        default_subwallet_id = WalletContract.default_subwallet_id(workchain, version)
        subwallet_id = self.__map_config_to_subwallet_id()
        subwallet_id = default_subwallet_id if subwallet_id is None else int(subwallet_id)

        return RecordBackup(name=self.name, address=self.address,
                            version=version,
                            workchain=workchain,
                            subwallet_id=subwallet_id,
                            mnemonics=" ".join(self.mnemonics), comment=self.comment)

    def __supported_wallet(self):
        return self.kind in self.kind_version_map

    def __map_kind_to_version(self):
        return self.kind_version_map.get(self.kind, None)

    def __map_config_to_workchain(self):
        # "wc=0,walletId=698983191,pk=qweqweqwe"
        return self.config.split(",")[0].split("=")[1]

    def __map_config_to_subwallet_id(self):
        temp = self.config.split("walletId=")
        if len(temp) == 2:
            return temp[1].split(",")[0]

        return None

    @property
    def kind_version_map(self) -> Dict:
        return {
            "org.ton.wallets.v2": WalletVersionEnum.v2r1,
            "org.ton.wallets.v2.r2": WalletVersionEnum.v2r2,
            "org.ton.wallets.v3": WalletVersionEnum.v3r1,
            "org.ton.wallets.v3.r2": WalletVersionEnum.v3r2,
        }


class RecordBackup(BaseModel):
    name: str
    address: Union[str, Address]
    version: WalletVersionEnum
    workchain: int
    subwallet_id: Optional[int]
    mnemonics: str
    comment: Optional[str] = ""

    class Config:
        use_enum_values = True
        validate_assignment = True
        arbitrary_types_allowed = True

    @classmethod
    def from_record(cls, record: "Record", mnemonics: str) -> "RecordBackup":
        return cls(
            name=record.name,
            address=record.address,
            version=record.version,
            workchain=record.workchain,
            subwallet_id=record.subwallet_id,
            mnemonics=mnemonics,
            comment=record.comment,
        )


class KeystoreBackup(BaseModel):
    version: int = settings.CURRENT_KEYSTORE_VERSION
    records: List[RecordBackup]
    contacts: List[WhitelistContact] = []

    @classmethod
    def backup_json(cls, keystore: BaseKeyStore) -> Dict:
        records: List[RecordBackup] = []
        for record in keystore.get_records(False):
            mnemonics = keystore.get_secret(record)
            records.append(RecordBackup.from_record(record, mnemonics))

        return cls(records=records, contacts=keystore.contacts, version=keystore.version).dict()

    @classmethod
    def restore_from_tons(cls, json_data: Union[Dict, List]) -> 'KeystoreBackup':
        records: List[RecordBackup] = []
        contacts: List[WhitelistContact] = []

        version = 1 if isinstance(json_data, list) else json_data["version"]

        if version == 1:
            raw_records = json_data
        else:
            raw_records = json_data['records']

        raw_contacts = []
        if version >= 4:
            raw_contacts = json_data['contacts']

        for raw_record in raw_records:
            records.append(RecordBackup.parse_obj(raw_record))

        for raw_contact in raw_contacts:
            contacts.append(WhitelistContact.parse_obj(raw_contact))

        return cls(records=records, contacts=contacts, version=version)

    @classmethod
    def restore_from_ton_cli(cls, json_data: Dict) -> 'KeystoreBackup':
        records: List[RecordBackup] = []
        for raw_record in json_data:
            backup_record = TonCliRecordBackup.parse_obj(
                raw_record).to_backup_record()
            if backup_record:
                records.append(backup_record)

        return cls(records=records, contacts=[])
