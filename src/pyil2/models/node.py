from typing import Dict, List

from pydantic import Field
from .base import BaseCamelModel

class SoftwareVersionModel(BaseCamelModel):
    """
    Version of the IL2 node.
    """
    
    core_libs: str
    """
    Version of the core libs.
    """
    main: str
    """
    Version of the node.
    """
    peer2peer: str
    """
    Version of the P2P.
    """
    tags: str
    """
    Version of the IL2 tags.
    """
    

class BaseNodeModel(BaseCamelModel):
    id: str
    """
    Unique node ID.
    """
    name: str
    """
    Node name.
    """
    network: str
    """
    Network this node participates on.
    """
    owner_id: str
    """
    Node owner ID.
    """
    owner_name: str
    """
    Node owner name.
    """
    roles: List[str] = Field(default_factory=list)
    """
    List of active roles running in the node.
    """
    color: str
    """
    Mapping color.
    """
    software_versions: SoftwareVersionModel
    """
    Version of software running the node.
    """
    extensions: Dict[str, str] = Field(default_factory=dict)
    """
    Dictionary with values for extensions on node configuration.
    """

class NodeDetailsModel(BaseNodeModel):
    chains: List[str] = Field(default_factory=list)
    """
    List of chains (only the IDs) in the node.
    """
    peer_address: str
    """
    Peer address.
    """

class PeerNodeModel(BaseNodeModel):
    address: str
    """
    Network address to contact the peer.
    """
    port: int = 0
    """
    Port the peer is listening.
    """