from .base import BaseApi
from ..models.errors import ErrorDetailsModel
from ..models.record import OpaqueRecordModel

class OpaqueApi(BaseApi):
    '''
    API class for the opaque requests.

    Args:
        client (`:obj:`IL2Client`): IL2Client to be used to send requests.
    
    Attributes:
        base_url (`str`): Base path of the requests.
    '''
    base_url='opaque/'

    def add_opaque(self, 
            chain_id: str,
            application_id: int,
            payload_type_id: int,
            payload: bytes,
            last_changed_serial: int=None,
        ) -> OpaqueRecordModel | ErrorDetailsModel:
        """
        Add an opaque record in a chain.

        If the `last_changed_serial` is passed, it will fail to add the opaque record \
            if the last record serial in the chain is not equal to the value passed.
        If `None` is passed, no verification is made.

        Args:
            chain_id (`str`): Chain ID.
            application_id (`int`): Application ID for the block.
            payload_type_id (`int`): The payload's Type ID.
            payload (`bytes`): Payload bytes.
            last_changed_serial (:obj:`int`): The serial number that the last record in the chain must be equal.

        Returns:
            [:obj:`models.record.OpaqueRecordModel`]: Opaque record details.
        """
        params = {
            "appId": application_id,
            "payloadTypeId": payload_type_id,
        }
        if last_changed_serial is not None:
            params['lastChangedRecordSerial'] = last_changed_serial
        
        resp = self._client._request(
            f'{self.base_url}{chain_id}',
            method='post',
            content_type='application/octet-stream',
            data=payload,
            params=params
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return OpaqueRecordModel(**resp.json())