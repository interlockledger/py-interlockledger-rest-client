from typing import List

from ..models.base import ListModel
from ..models.errors import ErrorDetailsModel
from ..models.records import (
    InterlockingRecordModel,
    ForceInterlockModel,
)
from ..models import (
    chain as chain_models,
    keys as keys_models,
)

from .base import BaseApi

class ChainApi(BaseApi):
    base_url='chain'

    def list_chains(self) -> List[chain_models.ChainIdModel] | ErrorDetailsModel:
        """
        Get a list of chains in the node.

        Returns:
            [:obj:`models.chain.NodeDetailsModel`]: List of chains in the node.
        """
        resp = self._client._request(
            url=f'{self.base_url}',
            method='get',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return chain_models.ChainIdModel.validate_list_python(resp.json())

    def create_chain(self, new_chain: chain_models.ChainCreationModel) -> chain_models.ChainCreatedModel | ErrorDetailsModel:
        """
        Create a new chain.

        Args:
            model (:obj:`models.chain.ChainCreationModel`): Model with the new chain attrbutes.

        Returns:
            :obj:`models.chain.ChainCreatedModel`: Chain created model.
        """
        if not isinstance(new_chain, chain_models.ChainCreationModel):
            raise ValueError("'new_chain' must be a ChainCreationModel.")
        
        resp = self._client._request(
            url=f'{self.base_url}',
            method='post',
            body=new_chain.model_dump(exclude_none=True, by_alias=True)
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return chain_models.ChainCreatedModel(**resp.json())

    def summary(self, chain_id: str) -> chain_models.ChainSummaryModel | ErrorDetailsModel:
        """
        Get the chain details by ID.

        Args:
            chain_id (:obj:`str`): Chain ID.
        
        Returns:
            :obj:`models.chain.ChainSummaryModel`: Chain details.
        """
        resp = self._client._request(
            url=f'{self.base_url}/{chain_id}',
            method='get',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return chain_models.ChainSummaryModel(**resp.json())
    
    def list_active_apps(self, chain_id: str) -> List[int] | ErrorDetailsModel:
        """
        Get the list os active apps in the chain.

        Args:
            chain_id (:obj:`str`): Chain ID.
        
        Returns:
            [:obj:`int`]: Enumerate apps that are currently permitted in this chain.
        """
        resp = self._client._request(
            url=f'{self.base_url}/{chain_id}/activeApps',
            method='get',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return resp.json()

    def add_active_apps(self, chain_id: str, apps_to_permit: List[int]) -> List[int] | ErrorDetailsModel:
        """
        Get the list os active apps in the chain.

        Args:
            chain_id (:obj:`str`): Chain ID.
        
        Returns:
            [:obj:`int`]: Enumerate apps that are currently permitted in this chain.
        """
        resp = self._client._request(
            url=f'{self.base_url}/{chain_id}/activeApps',
            method='post',
            body=apps_to_permit
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return resp.json()
    
    def list_interlockings(self,
            chain_id: str,
            page: int=0,
            size: int=10,
            how_many_from_last: int=0,
        ) -> ListModel[InterlockingRecordModel] | ErrorDetailsModel:
        """
        Get list of interlocks registered in the chain.

        Args:
            chain_id (:obj:`str`): Chain ID.
            page (:obj:`int`): Page to return.
            size (:obj:`int`): Number of items per page.
            how_many_from_last (:obj:`int`): How many interlocking records to return. If ommited or 0 returns all.

        Returns:
            :obj:`models.ListModel[models.records.InterlockingRecordModel]`: List of interlocking records.
        """
        params = {
            "howManyFromLast": how_many_from_last,
            "page": page,
            "pageSize": size
        }
        resp = self._client._request(
            url=f'{self.base_url}/{chain_id}/interlockings',
            method='get',
            params=params
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return ListModel[InterlockingRecordModel](**resp.json())
    
    def force_interlocking(self, chain_id: str, interlock: ForceInterlockModel) -> InterlockingRecordModel | ErrorDetailsModel:
        """
        Forces an interlock on a target chain.

        Args:
            chain_id (:obj:`str`): Chain ID.
            interlock (:obj:`models.records.ForceInterlockModel`): Force interlock details.

        Returns:
            :obj:`models.records.InterlockingRecordModel`: Interlocking details.
        """
        if not isinstance(interlock, ForceInterlockModel):
            raise ValueError("'interlock' must be a ForceInterlockModel.")
        
        resp = self._client._request(
            url=f'{self.base_url}/{chain_id}/interlockings',
            method='post',
            body=interlock.model_dump(exclude_none=True, by_alias=True)
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return InterlockingRecordModel(**resp.json())
    
    def list_keys(self, chain_id: str) -> List[keys_models.KeyDetailsModel] | ErrorDetailsModel:
        """
        List keys that are currently permitted in the chain.

        Args:
            chain_id (:obj:`str`): Chain ID.
        
        Returns:
            [:obj:`models.keys.KeyDetailsModel`]: List of key details.
        """
        resp = self._client._request(
            url=f'{self.base_url}/{chain_id}/key',
            method='get',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return keys_models.KeyDetailsModel.validate_list_python(resp.json())
    
    def add_keys(self, 
            chain_id: str,
            keys_to_permit: List[keys_models.KeyDetailsModel]
        ) -> List[keys_models.KeyDetailsModel] | ErrorDetailsModel:
        """
        Add keys to the permitted list for the chain.
        
        Args:
            chain_id (:obj:`str`): Chain ID.
            keys_to_permit ([:obj:`models.keys.KeyPermitModel`]): List of keys to permitted.
        
        Returns:
            [:obj:`models.keys.KeyDetailsModel`]: List of key details.
        """
        if not isinstance(keys_to_permit, list):
            raise ValueError("'keys_to_permit' must be a list of KeyDetailsModel.")
        body = []
        for item in keys_to_permit:
            if not isinstance(item, keys_models.KeyDetailsModel):
                raise ValueError("'keys_to_permit' must be a list of KeyDetailsModel.")
            body.append(item.model_dump(exclude_none=True, by_alias=True))
        resp = self._client._request(
            url=f'{self.base_url}/{chain_id}/key',
            method='post',
            body=body,
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return keys_models.KeyDetailsModel.validate_list_python(resp.json())