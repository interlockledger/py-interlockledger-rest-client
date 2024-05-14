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
from typing import List

from ..models.chain import ChainIdModel
from ..models import node
from ..models.apps import AppsModel
from ..models.base import ListModel
from ..models.errors import ErrorDetailsModel
from ..models.record import InterlockingRecordModel

from .base import BaseApi


class NodeApi(BaseApi):
    '''
    API class for the node requests.

    Args:
        client (:obj:`pyil2.IL2Client`): IL2Client to be used to send requests.

    Attributes:
        base_url (`str`): Base path of the requests.
    '''
    base_url = ''

    @property
    def details(self) -> node.NodeDetailsModel | ErrorDetailsModel:
        """
        :obj:`pyil2.models.node.NodeDetailsModel`: Details about the node.
        """
        resp = self._client.request(
            url=f'{self.base_url}',
            method='get',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return node.NodeDetailsModel(**resp.json())

    @property
    def api_version(self) -> str | ErrorDetailsModel:
        """
        :obj:`str`: REST API version.
        """
        resp = self._client.request(
            url=f'{self.base_url}/apiVersion',
            method='get',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return resp.json()

    def list_apps(self) -> AppsModel | ErrorDetailsModel:
        """
        Get the list of valid apps in the network.

        Returns:
            :obj:`pyil2.models.apps.AppsModel`: Valid apps in the network.
        """
        resp = self._client.request(
            url=f'{self.base_url}/apps',
            method='get'
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return AppsModel(**resp.json())

    def list_interlockings_to_chain(
            self,
            chain_id: str,
            last_known_block: int = None,
            last_to_first: bool = False,
            page: int = 0,
            size: int = 10,
        ) -> ListModel[InterlockingRecordModel] | ErrorDetailsModel:
        """
        Get the list of interlocking records pointing to a target chain instance.

        Args:
            chain_id (:obj:`str`): Target chain id.
            last_known_block (:obj:`int`): Last known block to query.
            last_to_first  (:obj:`bool`): If `True`, return the items in reverse order.
            page  (:obj:`int`): Page to query.
            size  (:obj:`int`): Number of elements in the page.

        Returns:
            :obj:`pyil2.models.base.ListModel` \
                [:obj:`pyil2.models.record.InterlockingRecordModel`]: \
                List of interlocking records.
        """
        params = {
            "page": page,
            "pageSize": size,
            "lastToFirst": last_to_first,
        }
        if last_known_block is not None:
            params['lastKnownBlock'] = last_known_block
        resp = self._client.request(
            url=f'{self.base_url}/interlockings/{chain_id}',
            method='get',
            params=params,
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return ListModel[InterlockingRecordModel](**resp.json())

    def list_peers(self) -> List[node.PeerNodeModel] | ErrorDetailsModel:
        """
        Get the list of known peer nodes.

        Returns:
            [:obj:`pyil2.models.node.PeerNodeModel`]: List of peers.
        """
        resp = self._client.request(
            url=f'{self.base_url}/peers',
            method='get',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return node.PeerNodeModel.validate_list_python(resp.json())

    def list_mirrors(self) -> List[ChainIdModel] | ErrorDetailsModel:
        """
        List of mirror instances.

        Returns:
            [:obj:`pyil2.models.chain.ChainIdModel`]: List of mirrors.
        """
        resp = self._client.request(
            url=f'{self.base_url}/mirrors',
            method='get',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return ChainIdModel.validate_list_python(resp.json())

    def add_mirrors(self, chains: List[str]) -> bool | ErrorDetailsModel:
        """
        Add chain mirrors to the node.

        Args:
            chains ([:obj:`str`]): List of chain IDs.

        Returns:
            [:obj:`bool`]: Returns `True` if success.
        """
        resp = self._client.request(
            url=f'{self.base_url}/mirrors',
            method='post',
            body=chains
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return True
