from .base import BaseApi

from ..models.errors import ErrorDetailsModel
from ..models import documents as documents_models

class DocumentsApi(BaseApi):
    '''
    API class for the Multi-Documents requests.

    Args:
        client (`:obj:`IL2Client`): IL2Client to be used to send requests.
    
    Attributes:
        base_url (`str`): Base path of the requests.
    '''
    base_url='documents'

    @property
    def documents_configuration(self) -> documents_models.DocumentUploadConfigurationModel:
        """
        :obj:`models.documents.DocumentUploadConfigurationModel`: Documents upload configuration.
        """
        resp = self._client._request(
            f'{self.base_url}/configuration',
            method='get'
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return documents_models.DocumentUploadConfigurationModel(**resp.json())