from typing import (
    Dict, 
    Any,
)
from .base import BaseApi
from ..models.errors import ErrorDetailsModel
from ..models.json import JsonDocumentModel

class JsonApi(BaseApi):
    '''
    API class for the JSON documents requests.

    Args:
        client (`:obj:`IL2Client`): IL2Client to be used to send requests.
    
    Attributes:
        base_url (`str`): Base path of the requests.
    '''
    base_url='jsonDocuments@'

    def add_json_document(self, chain_id: str, payload: Dict[str, Any]) -> JsonDocumentModel | ErrorDetailsModel:
        """
        Add a JSON document record encrypted with the client certificate used in the request.

        Args:
            chain_id (:obj:`str`): Chain ID.
            payload ({:obj:`str`: Any}): A valid JSON in dictionary format.
        
        Returns:
            :obj:`models.json.JsonDocumentModel`: Added JSON document details.
        """
        resp = self._client._request(
            f'{self.base_url}{chain_id}',
            method='post',
            body=payload,
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return JsonDocumentModel(**resp.json())
