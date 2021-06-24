from pydantic import Field
from pybitcoin import Model


class GeneralInfoRequest(Model):
    """A request model used for the /wallet/general-info endpoint.

    Args:
        name (str): The name of the wallet.
    """
    name: str = Field(alias='Name')
