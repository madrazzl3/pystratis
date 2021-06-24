from typing import Optional
from pydantic import Field
from pybitcoin import Model


class AccountRequest(Model):
    """A request model used for the /wallet/transactioncount endpoint.

    Args:
        wallet_name (str): The name of wallet to retrieve info from.
        account_name (str, optional): The name of the account to retrieve info for.
    """
    wallet_name: str = Field(alias='WalletName')
    account_name: Optional[str] = Field(default='account 0', alias='AccountName')
