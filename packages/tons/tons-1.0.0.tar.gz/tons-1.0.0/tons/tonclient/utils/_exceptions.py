class TonconnectInvalidNetworkError(Exception):
    pass


class TonconnectUnsupportedMethodError(Exception):
    pass


class TonconnectBadRequestError(Exception):
    pass


class TonconnectDifferentNetworkError(Exception):
    pass


class TonconnectWrongMessagesNumberError(Exception):
    pass


class TonconnectWrongRpcRequestIdError(Exception):
    pass


class TonconnectRequestExpiredError(Exception):
    pass



class TonconnectWrongParamsNumberError(Exception):
    pass


class ConnectionAlreadyExistsError(Exception):
    pass


class ConnectionDoesNotExistError(Exception):
    pass


class WhitelistContactAlreadyExistsError(Exception):
    pass


class WhitelistContactDoesNotExistError(Exception):
    pass


class WhitelistContactNameInvalidError(ValueError):
    pass


class KeyStoreAlreadyExistsError(Exception):
    pass


class KeyStoreDoesNotExistError(Exception):
    pass


class KeyStoreAccessDeniedError(Exception):
    pass


class KeyStoreInvalidPasswordError(Exception):
    pass


class KeyStoreNameInvalidError(ValueError):
    pass


class InvalidKeyStoreError(Exception):
    pass


class KeyStoreIsNotSpecifiedError(Exception):
    pass


class RecordAlreadyExistsError(Exception):
    pass


class RecordDoesNotExistError(Exception):
    pass


class RecordNameInvalidError(ValueError):
    pass


class InvalidMnemonicsError(ValueError):
    pass
