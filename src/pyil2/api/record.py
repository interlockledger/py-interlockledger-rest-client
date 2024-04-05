from typing import List

from ..models.base import ListModel
from ..models.errors import ErrorDetailsModel
from ..models import (
    chain as chain_models,
    keys as keys_models,
    record as record_models,
)

from .base import BaseApi

class RecordApi(BaseApi):
    base_url='records@'

    def list_records(self,
            chain_id: str,
            first_serial: int=None,
            last_serial: int=None,
            last_to_first: bool=False,
            ommit_payload: bool=False,
            page: int=0,
            size: int=10,
        ) -> ListModel[record_models.RecordModel] | ErrorDetailsModel:
        """
        Get a list of records in a chain.

        Args:
            chain_id (`str`): Chain ID.
            first_serial (`int`): Serial number of first record to read. Default: First in whole chain.
            last_serial (`int`): Serial number of last record to read. Default: Last in whole chain.
            last_to_first (`bool`): If `True`, return the items in reverse order.
            ommit_payload (`bool`): If `True`, ommits the payload in the response.
            page (:obj:`int`): Page to return.
            size (:obj:`int`): Number of items per page.

        Returns:
            [:obj:`models.record.RecordModel`]: List of records in a chain.
        """
        params = {
            "page": page,
            "pageSize": size,
            "lastToFirst": last_to_first,
            "ommitPayload": ommit_payload,
        }
        if first_serial is not None:
            params['firstSerial'] = first_serial
        if last_serial is not None:
            params['lastSerial'] = last_serial
        
        resp = self._client._request(
            url=f'{self.base_url}{chain_id}',
            method='get',
            params=params,
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return ListModel[record_models.RecordModel](**resp.json())

    def add_record(self,
            chain_id: str,
            new_record: record_models.NewRecordModel
        ) -> record_models.RecordModel | ErrorDetailsModel:
        """
        Add a new record using raw bytes. 
        The payload must be in the correct application ID format in Base64.
        
        Note: Use this method only if you know the payload format. \
            We highly recommend to use the applications APIs to insert records.

        Args:
            chain_id (`str`): Chain ID.
            new_record (:obj:`models.record.NewRecordModel`): Model with the description of the new record.
        
        Returns:
            :obj:`models.record.RecordModel`: Added record model.
        """
        if not isinstance(new_record, record_models.NewRecordModel):
            raise ValueError("'new_record' must be a NewRecordModel.")
        resp = self._client._request(
            url=f'{self.base_url}{chain_id}',
            method='post',
            body=new_record.model_dump(exclude_none=True, by_alias=True)
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return record_models.RecordModel(**resp.json())

    def get_record_at(self,
            chain_id: str,
            serial: int,
        ) -> record_models.RecordModel | ErrorDetailsModel:
        """
        Get a record by serial number.

        Args:
            chain_id (`str`): Chain ID.
            serial (`int`): Record serial number.

        Returns:
            [:obj:`models.record.RecordModel`]: Record in a chain.
        """
        resp = self._client._request(
            url=f'{self.base_url}{chain_id}/{serial}',
            method='get',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return record_models.RecordModel(**resp.json())

    def query_records(self,
            chain_id: str,
            query: str,
            how_many: int=None,
            last_to_first: bool=False,
            ommit_payload: bool=False,
            page: int=0,
            size: int=10,
        ) -> ListModel[record_models.RecordModel] | ErrorDetailsModel:
        """
        Query records in a chain using the InterlockQL language.

        Args:
            chain_id (`str`): Chain ID.
            query (`str`): Query in the InterlockQL language.
            how_many (`int`): How many records to return. If ommited or 0 returns all.
            last_to_first (`bool`): If `True`, return the items in reverse order.
            ommit_payload (`bool`): If `True`, ommits the payload in the response.
            page (:obj:`int`): Page to return.
            size (:obj:`int`): Number of items per page.

        Returns:
            [:obj:`models.record.RecordModel`]: List of records in a chain.
        """
        params = {
            "queryAsInterlockQL": query,
            "page": page,
            "pageSize": size,
            "lastToFirst": last_to_first,
            "ommitPayload": ommit_payload,
        }
        if how_many is not None:
            params['howMany'] = how_many
        
        resp = self._client._request(
            url=f'{self.base_url}{chain_id}/query',
            method='get',
            params=params,
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return ListModel[record_models.RecordModel](**resp.json())
    
    def list_records_as_json(self,
            chain_id: str,
            first_serial: int=None,
            last_serial: int=None,
            last_to_first: bool=False,
            page: int=0,
            size: int=10,
        ) -> ListModel[record_models.RecordAsJsonModel] | ErrorDetailsModel:
        """
        Get a list of records in a chain with the payload mapped to a JSON format.

        Args:
            chain_id (`str`): Chain ID.
            first_serial (`int`): Serial number of first record to read. Default: First in whole chain.
            last_serial (`int`): Serial number of last record to read. Default: Last in whole chain.
            last_to_first (`bool`): If `True`, return the items in reverse order.
            page (:obj:`int`): Page to return.
            size (:obj:`int`): Number of items per page.

        Returns:
            [:obj:`models.record.RecordAsJsonModel`]: List of records in a chain with the payload as JSON.
        """
        params = {
            "page": page,
            "pageSize": size,
            "lastToFirst": last_to_first,
        }
        if first_serial is not None:
            params['firstSerial'] = first_serial
        if last_serial is not None:
            params['lastSerial'] = last_serial
        
        resp = self._client._request(
            url=f'{self.base_url}{chain_id}/asJson',
            method='get',
            params=params,
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return ListModel[record_models.RecordAsJsonModel](**resp.json())