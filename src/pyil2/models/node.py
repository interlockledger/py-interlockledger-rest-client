from typing import Dict, List

from pydantic import Field
from .base import BaseCamelModel

class SoftwerVersionModel(BaseCamelModel):
    core_libs: str
    main: str
    peer2peer: str
    tags: str

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
    software_versions: SoftwerVersionModel
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
    port: int
    """
    Port the peer is listening.
    """