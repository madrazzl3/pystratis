import json
from pybitcoin import Model


class ClearBannedRequest(Model):
    """A request model for the network/clearbanned endpoint."""
    def json(self, *args, **kwargs):
        return json.dumps(True)
