from pydantic import SecretStr
from pybitcoin import Model


class LoadRequest(Model):
    """A request model used for the /wallet/load endpoint.

    Args:
        name (str): The name of the wallet.
        password (SecretStr): The password of the wallet.
    """
    name: str
    password: SecretStr
