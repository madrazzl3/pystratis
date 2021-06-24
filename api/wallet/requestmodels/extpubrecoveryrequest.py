from typing import Optional
from pydantic import Field, conint
from pybitcoin import Model, ExtPubKey


class ExtPubRecoveryRequest(Model):
    """A request model used for the /wallet/recover-via-extpubkey endpoint.

    Args:
        extpubkey (ExtPubKey): The extended public key used to recover wallet.
        account_index (conint(ge=0)): The index of extended public key.
        name (str): The name of the wallet.
        creation_date (str, optional): The creation date of the wallet.
    """
    extpubkey: ExtPubKey = Field(alias='extPubKey')
    account_index: conint(ge=0) = Field(alias='accountIndex')
    name: str
    creation_date: Optional[str] = Field(default=None, alias='creationDate')
