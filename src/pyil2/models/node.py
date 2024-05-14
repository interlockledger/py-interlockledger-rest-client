# Copyright (c) 2024, InterlockLedger Network
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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
    """
    Base node details model.
    """

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
    """
    Node details model.
    """

    chains: List[str] = Field(default_factory=list)
    """
    List of chains (only the IDs) in the node.
    """
    peer_address: str
    """
    Peer address.
    """


class PeerNodeModel(BaseNodeModel):
    """
    Peer node details model.
    """

    address: str
    """
    Network address to contact the peer.
    """
    port: int = 0
    """
    Port the peer is listening.
    """
