from typing import List
from ..models import node
from ..models.apps import AppsModel

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

    def apps(self):
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