from typing import List
from ..models import node
from .base import BaseApi

class NodeApi(BaseApi):
    base_url=''

    def details(self) -> node.NodeDetailsModel:
        """
        Get the node details.

        Returns:
            :obj:`models.node.NodeDetailsModel`: Details about the node.
        """
        resp = self._client._request(
            url=f'{self.base_url}',
            method='get',
        )
        if resp.status_code != 200:
            raise Exception
        return node.NodeDetailsModel(**resp.json())

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