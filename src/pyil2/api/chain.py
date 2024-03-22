from typing import List

from ..models.base import ListModel
from ..models import chain as chain_models

from .base import BaseApi

class ChainApi(BaseApi):
    base_url='chain'

    def list_chains(self) -> List[chain_models.ChainIdModel]:
        """
        Get a list of chains in the node.

        Returns:
            [:obj:`models.chain.NodeDetailsModel`]: List of chains in the node.
        """
        resp = self._client._request(
            url=f'{self.base_url}',
            method='get',
        )
        if resp.status_code != 200:
            raise Exception
        return chain_models.ChainIdModel.validate_list_python(resp.json())
