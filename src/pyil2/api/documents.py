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

    def begin_document_transaction(self,
            new_transaction: documents_models.BeginDocumentTransactionModel
        ) -> documents_models.DocumentTransactionModel:
        """
        Begin a document upload transaction.

        The transaction will rollback on timeout or errors.

        Args:
            new_transaction (:obj:`models.documents.BeginDocumentTransactionModel`): Begin transaction details.
        
        Returns:
            :obj:`models.documents.BeginDocumentTransactionModel`: Document upload transaction status.
        """
        if not isinstance(new_transaction, documents_models.BeginDocumentTransactionModel):
            raise ValueError("'new_transaction' must be a BeginDocumentTransactionModel.")
        
        resp = self._client._request(
            f'{self.base_url}/transaction',
            method='post',
            body=new_transaction.model_dump(by_alias=True, exclude_none=True)
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return documents_models.DocumentTransactionModel(**resp.json())