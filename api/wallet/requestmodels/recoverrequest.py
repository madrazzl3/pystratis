from typing import Optional
from pydantic import SecretStr, Field
from pybitcoin import Model


class RecoverRequest(Model):
    """A request model used for the /wallet/recover endpoint.

    Args:
        mnemonic (str): The mnemonic used to create this wallet.
        password (SecretStr): The password of the wallet.
        passphrase (SecretStr): The passphrase of the wallet.
        name: (str): The name for a wallet.
        creation_date (str, optional): The creation date of the wallet.
    """
    mnemonic: str
    password: SecretStr
    passphrase: SecretStr
    name: str
    creation_date: Optional[str] = Field(default=None, alias='creationDate')
