from typing import Optional
from pydantic import Field, validator
from pybitcoin import Model


class MaxBalanceRequest(Model):
    """A request model for the wallet/maxbalance endpoint.

    Args:
        wallet_name: str = Field(alias='WalletName')
        account_name: Optional[str] = Field(default='account 0', alias='AccountName')
        fee_type: str = Field(alias='FeeType')
        allow_unconfirmed: Optional[bool] = Field(default=False, alias='AllowUnconfirmed')
    """
    wallet_name: str = Field(alias='WalletName')
    account_name: Optional[str] = Field(default='account 0', alias='AccountName')
    fee_type: str = Field(alias='FeeType')
    allow_unconfirmed: Optional[bool] = Field(default=False, alias='AllowUnconfirmed')

    # noinspection PyMethodParameters,PyUnusedLocal
    @validator('fee_type')
    def validate_fee_type(cls, v, values):
        allowed = [
            'low',
            'medium',
            'high'
        ]
        if v is not None and v not in allowed:
            raise ValueError(f'Invalid command. Must be: {allowed}')
        return v
