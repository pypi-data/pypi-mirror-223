from pydantic import BaseModel

from ._dapp import DAppConfig, TonNetworkEnum


class ProviderConfig(BaseModel):
    dapp: DAppConfig = DAppConfig()

    class Config:
        validate_assignment = True


__all__ = [
    "DAppConfig",
    "TonNetworkEnum",
    "ProviderConfig",
]
