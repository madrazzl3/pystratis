from typing import Optional
from pydantic import BaseModel, Field, conint


class WalletGeneralInfoModel(BaseModel):
    """A model representing general wallet info.

    Args:
        wallet_name (str, optional): The name of the wallet.
        network (str): The name of network this wallet operating on.
        creation_time (str): The time this wallet was created.
        is_decrypted (bool): Is wallet decrypted or not.
        last_block_synced_height (conint(ge=0), optional): The height of the last block that was synced
        chain_tip (conint(ge=0), optional): The total number of blocks.
        is_chain_synced (bool): Whether the chain is synced with the network.
        connected_nodes (conint(ge=0)): The total number of nodes that we're connected to.
    """
    wallet_name: Optional[str] = Field(alias='walletName')
    network: str
    creation_time: str = Field(alias='creationTime')
    is_decrypted: bool = Field(alias='isDecrypted')
    last_block_synced_height: Optional[conint(ge=0)] = Field(alias='lastBlockSyncedHeight')
    chain_tip: Optional[conint(ge=0)] = Field(alias='chainTip')
    is_chain_synced: bool = Field(alias='isChainSynced')
    connected_nodes: conint(ge=0) = Field(alias='connectedNodes')

    class Config:
        allow_population_by_field_name = True

    def json(self, *args, **kwargs) -> str:
        return super().json(exclude_none=True, by_alias=True)
