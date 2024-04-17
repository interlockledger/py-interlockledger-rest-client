import os
import re
import shutil
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
    def documents_configuration(self) -> documents_models.DocumentUploadConfigurationModel | ErrorDetailsModel:
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
        ) -> documents_models.DocumentTransactionModel | ErrorDetailsModel:
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

    def get_document_transaction_status(self,
            transaction_id: str
        ) -> documents_models.DocumentTransactionModel | ErrorDetailsModel :
        """
        Get a document upload transaction status.

        Args:
            transaction_id (:obj:`str`): Document upload transaction ID.
        
        Returns:
            :obj:`models.documents.BeginDocumentTransactionModel`: Document upload transaction status.
        """
        resp = self._client._request(
            f'{self.base_url}/transaction/{transaction_id}',
            method='get',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return documents_models.DocumentTransactionModel(**resp.json())

    def upload_document(self, 
            transaction_id: str,
            filename: str,
            content_type: str,
            file_bytes: bytes,
            comment: str=None,
            relative_path: str="/",
        ) -> documents_models.DocumentTransactionModel | ErrorDetailsModel:
        """
        Add a file to a document upload transaction.

        Args:
            transaction_id (:obj:`str`): Document upload transaction ID.
            filename (:obj:`str`): File name.
            content_type (:obj:`str`): File mime-type
            file_bytes (:obj:`str`): File bytes.
            comment (:obj:`str`): Additional comment.
            relative_path (:obj:`str`): Relative path of the file inside the record.
        
        Returns:
            :obj:`models.documents.BeginDocumentTransactionModel`: Document upload transaction status.
        """
        params = {
            "name": filename,
            "path": relative_path,
        }
        if comment:
            params['comment'] = comment
        resp = self._client._request(
            f'{self.base_url}/transaction/{transaction_id}',
            method='post',
            params=params,
            content_type=content_type,
            data=file_bytes,
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return documents_models.DocumentTransactionModel(**resp.json())

    def commit_document_transaction(self, transaction_id: str) -> str | ErrorDetailsModel:
        """
        Commits a document upload transaction.

        Args:
            transaction_id (:obj:`str`): Document upload transaction ID.
        
        Returns:
            :obj:`str`: Document locator.
        """
        resp = self._client._request(
            f'{self.base_url}/transaction/{transaction_id}/commit',
            method='post',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return resp.json()

    def get_document_metadata(self, 
            locator: str
        ) -> documents_models.DocumentMetadataModel | ErrorDetailsModel:
        """
        Get the documents metadata by the locator.

        Args:
            locator (:obj:`str`): Document locator.
        
        Returns:
            :obj:`models.documents.DocumentMetadataModel`: Documents metadata.
        """
        resp = self._client._request(
            f'{self.base_url}/{locator}/metadata',
            method='get',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return documents_models.DocumentMetadataModel(**resp.json())

    def download_single_document_at(self, 
        locator: str,
        index: int,
        dst_path: str='./',
    ) -> str | ErrorDetailsModel:
        """
        Download a single document by position from the set of documents to a folder (default: current folder).

        Args:
            locator (:obj:`str`): A Documents Storage Locator.
            index (:obj:`int`): Index of the file.
            dst_path (:obj:`str`): Download the file to this folder.
        
        Returns:
            :obj:`str`: Downloaded file full path.
        """
        resp = self._client._download_file(
            f'{self.base_url}/{locator}/{index}',
            dst_path=dst_path
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return resp
    
    def download_documents_as_zip(self, 
        locator: str,
        dst_path: str='./',
    ) -> str | ErrorDetailsModel:
        """
        Download documents in a compressed file to a folder (default: current folder).

        Args:
            locator (:obj:`str`): A Documents Storage Locator.
            dst_path (:obj:`str`): Download the file to this folder.
        
        Returns:
            :obj:`str`: Downloaded file full path.
        """
        resp = self._client._download_file(
            f'{self.base_url}/{locator}/zip',
            dst_path=dst_path
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return resp
    
    