from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum
from typing import Optional, List, Tuple

from colorama import Fore
from pydantic import BaseModel, validator

from tons.tonsdk.utils import Address, InvalidAddressError
from tons.utils import storage
from ._exceptions import WhitelistContactAlreadyExistsError, WhitelistContactDoesNotExistError, \
    WhitelistContactNameInvalidError


class WhitelistContactType(Enum):
    keystore = 0
    global_ = 1
    local = 2


class WhitelistContact(BaseModel):
    name: str
    address: str
    default_message: str = ""

    class Config:
        validate_assignment = True

    @validator('address')
    def validate_address(cls, v, values, **kwargs):
        if v:
            try:
                Address(v)
                return v

            except InvalidAddressError as e:
                raise ValueError(e)

    @property
    def address_to_show(self) -> str:
        return Address(self.address).to_string(is_user_friendly=True)

    @staticmethod
    def pretty_string(name, contact_type):
        if contact_type == WhitelistContactType.keystore:
            return f"{Fore.GREEN}(w){Fore.RESET} {name}"

        if contact_type == WhitelistContactType.local:
            return f"{Fore.CYAN}(l){Fore.RESET} {name}"

        if contact_type == WhitelistContactType.global_:
            return f"{Fore.MAGENTA}(g){Fore.RESET} {name}"


class BaseWhitelist(ABC):
    def __init__(self, contacts: List[WhitelistContact]):
        self._contacts = contacts

    def get_contacts(self, sorted_contacts: bool) -> Tuple[WhitelistContact]:
        if sorted_contacts:
            return tuple(sorted(self._contacts, key=lambda contact: contact.name.lower()))
        return tuple(self._contacts)

    def add_contact(self, name: str, address: str, default_message: str = "", save: bool = False):
        if not name:
            raise WhitelistContactNameInvalidError('Contact name should not be empty')

        if self.get_contact(name) is not None:
            raise WhitelistContactAlreadyExistsError(f"Contact with the name '{name}' already exists")
        if (contact := self.get_contact_by_address(address)) is not None:
            raise WhitelistContactAlreadyExistsError(
                f"Contact with the address {address} already exists: {contact.name}")
        contacts_before = deepcopy(self._contacts)
        try:
            self._contacts.append(WhitelistContact(name=name,
                                                   address=address,
                                                   default_message=default_message))
            if save:
                self.save(contacts_before)
        except:
            self._contacts = contacts_before
            raise

    def get_contact(self, name: str, raise_none: bool = False) -> Optional[WhitelistContact]:
        contact = next((contact for contact in self._contacts if contact.name == name), None)
        if contact is None and raise_none:
            raise WhitelistContactDoesNotExistError(f"Contact with the name {name} does not exist")
        return contact

    def get_contact_by_address(self, address: str, raise_none: bool = False) -> Optional[WhitelistContact]:
        contact = next((contact for contact in self._contacts if Address(contact.address) == Address(address)), None)
        if contact is None and raise_none:
            raise WhitelistContactDoesNotExistError(f"Contact with the address {address} does not exist")
        return contact

    def edit_contact(self, name: str, new_name: Optional[str] = None, new_address: Optional[str] = None,
                     new_default_message: Optional[str] = None, save: bool = False):
        contact = self.get_contact(name, raise_none=True)
        contact_idx = self._contacts.index(contact)
        contacts_before = deepcopy(self._contacts)

        try:
            if new_name:
                if new_name != name and self.get_contact(new_name, raise_none=False) is not None:
                    raise WhitelistContactAlreadyExistsError(f"Contact with the name '{new_name}' already exists")
                self._contacts[contact_idx].name = new_name

            if new_address:
                if Address(contact.address) != Address(new_address) and \
                        self.get_contact_by_address(new_address, raise_none=False) is not None:
                    raise WhitelistContactAlreadyExistsError(f"Contact with the address {new_address} already exists")
                self._contacts[contact_idx].address = new_address

            if new_default_message:
                self._contacts[contact_idx].default_message = new_default_message

            if save:
                self.save(contacts_before)
        except:
            self._contacts = contacts_before
            raise

    def delete_contact_by_name(self, name: str, save: bool = False) -> WhitelistContact:
        contact = self.get_contact(name, raise_none=True)
        self.delete_contact(contact, save)
        return contact

    def delete_contact(self, contact: WhitelistContact, save: bool = False):
        contacts_before = deepcopy(self._contacts)
        self._contacts.remove(contact)
        if save:
            self.save(contacts_before)

    @abstractmethod
    def save(self, contacts_before: Optional[List[WhitelistContact]] = None):
        raise NotImplementedError


class GlobalWhitelist(BaseWhitelist):
    def __init__(self, whitelist_path: str):
        try:
            contacts_json = storage.read_json(whitelist_path)
        except FileNotFoundError:
            contacts = []
        else:
            if contacts_json:
                contacts = [WhitelistContact.parse_obj(contact)
                            for contact in contacts_json]
            else:
                contacts = []

        super().__init__(contacts)
        self.whitelist_path = whitelist_path

    def save(self, contacts_before: Optional[List[WhitelistContact]] = None):
        try:
            storage.save_json(self.whitelist_path, [contact.dict() for contact in self._contacts])
        except Exception:
            if contacts_before:
                self._contacts = contacts_before
            raise


class LocalWhitelist(BaseWhitelist):
    def __init__(self, contacts, keystore):
        super().__init__(contacts)
        self.keystore = keystore

    def add_contact(self, name: str, address: str, default_message: str = "", save: bool = False):
        res = super().add_contact(name, address, default_message, save)
        self.keystore.contacts = self._contacts
        return res

    def edit_contact(self, name: str, new_name: Optional[str] = None, new_address: Optional[str] = None,
                     new_default_message: Optional[str] = None, save: bool = False):
        res = super().edit_contact(name, new_name, new_address, new_default_message, save)
        self.keystore.contacts = self._contacts
        return res

    def delete_contact_by_name(self, name: str, save: bool = False) -> WhitelistContact:
        res = super().delete_contact_by_name(name, save)
        self.keystore.contacts = self._contacts
        return res

    def delete_contact(self, contact: WhitelistContact, save: bool = False):
        res = super().delete_contact(contact, save)
        self.keystore.contacts = self._contacts
        return res

    def save(self, contacts_before: Optional[List[WhitelistContact]] = None):
        self.keystore.save(contacts_before=contacts_before)
