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

    