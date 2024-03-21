from typing import List
from ..models import node
from ..models.apps import AppsModel
from ..models.base import ListModel
from ..models.records import InterlockingRecordModel

from .base import BaseApi

class NodeApi(BaseApi):
    base_url=''

    @property
    def details(self) -> node.NodeDetailsModel:
        """
        :obj:`models.node.NodeDetailsModel`: Details about the node.
        """
        resp = self._client._request(
            url=f'{self.base_url}',
            method='get',
        )
        if resp.status_code != 200:
            raise Exception
        return node.NodeDetailsModel(**resp.json())

    @property
    def api_version(self) -> str:
        """
        :obj:`str`: REST API version.
        """
        resp = self._client._request(
            url=f'{self.base_url}/apiVersion',
            method='get',
        )
        if resp.status_code != 200:
            raise Exception
        return resp.json()

    def peers(self) -> List[node.PeerNodeModel]:
        """
        Get the list of known peer nodes.

        Returns:
            [:obj:`models.node.PeerNodeModel`]: List of peers.
        """
        resp = self._client._request(
            url=f'{self.base_url}/peers',
            method='get',
        )
        if resp.status_code != 200:
            raise Exception
        return node.PeerNodeModel.validate_list_python(resp.json())

    def apps(self) -> AppsModel:
        """
        Get the list of valid apps in the network.

        Returns:
            :obj:`models.apps.AppsModel`: Valid apps in the network.
        """
        resp = self._client._request(
            url=f'{self.base_url}/apps',
            method='get'
        )
        if resp.status_code != 200:
            raise Exception
        return AppsModel(**resp.json())

    def interlockings(self,
            chain_id: str,
            last_known_block: int=None,
            last_to_first: bool=False,
            page: int=0,
            size: int=10,
        ) -> ListModel[InterlockingRecordModel]:
        """
        Get the list of interlocking records pointing to a target chain instance.

        Args:
            chain_id (:obj:`str`): Target chain id.
            last_known_block (:obj:`int`): Last known block to query.
            last_to_first  (:obj:`bool`): If `True`, return the items in reverse order.
            page  (:obj:`int`): Page to query.
            size  (:obj:`int`): Number of elements in the page.

        Returns:
            :obj:`models.ListModel[models.records.InterlockingRecordModel]`: List of interlocking records.
        """
        params = {
            "page": page,
            "pageSize": size,
            "lastToFirst": last_to_first,
        }
        if last_known_block is not None:
            params['lastKnownBlock'] = last_known_block
        resp = self._client._request(
            url=f'{self.base_url}/interlockings/{chain_id}',
            method='get',
            params=params,
        )
        if resp.status_code != 200:
            raise Exception
        return ListModel[InterlockingRecordModel](**resp.json())