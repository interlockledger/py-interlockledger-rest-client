# Copyright (c) 2024, InterlockLedger Network
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import os
import mimetypes
import requests
from .base import BaseApi

from ..models.errors import ErrorDetailsModel
from ..models import documents as documents_models


class DocumentsApi(BaseApi):
    '''
    API class for the Multi-Documents requests.

    Args:
        client (:obj:`pyil2.IL2Client`): IL2Client to be used to send requests.

    Attributes:
        base_url (`str`): Base path of the requests.
    '''
    base_url = 'documents'

    @property
    def documents_configuration(self) -> documents_models.DocumentUploadConfigurationModel |\
                                        ErrorDetailsModel:
        """
        :obj:`pyil2.models.documents.DocumentUploadConfigurationModel`: \
            Documents upload configuration.
        """
        resp = self._client.request(
            f'{self.base_url}/configuration',
            method='get'
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return documents_models.DocumentUploadConfigurationModel(**resp.json())

    def begin_document_transaction(
            self,
            new_transaction: documents_models.BeginDocumentTransactionModel
        ) -> documents_models.DocumentTransactionModel | ErrorDetailsModel:
        """
        Begin a document upload transaction.

        The transaction will rollback on timeout or errors.

        Args:
            new_transaction (:obj:`pyil2.models.documents.BeginDocumentTransactionModel`): \
                Begin transaction details.

        Returns:
            :obj:`pyil2.models.documents.DocumentTransactionModel`: Document upload \
                transaction status.
        """
        if not isinstance(new_transaction, documents_models.BeginDocumentTransactionModel):
            raise ValueError(
                "'new_transaction' must be a BeginDocumentTransactionModel.")

        resp = self._client.request(
            f'{self.base_url}/transaction',
            method='post',
            body=new_transaction.model_dump(by_alias=True, exclude_none=True)
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return documents_models.DocumentTransactionModel(**resp.json())

    def get_document_transaction_status(
            self,
            transaction_id: str
        ) -> documents_models.DocumentTransactionModel | ErrorDetailsModel:
        """
        Get a document upload transaction status.

        Args:
            transaction_id (:obj:`str`): Document upload transaction ID.

        Returns:
            :obj:`pyil2.models.documents.DocumentTransactionModel`: Document upload \
                transaction status.
        """
        resp = self._client.request(
            f'{self.base_url}/transaction/{transaction_id}',
            method='get',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return documents_models.DocumentTransactionModel(**resp.json())

    def upload_document(
            self,
            transaction_id: str,
            filename: str,
            content_type: str,
            file_bytes: bytes,
            comment: str = None,
            relative_path: str = "/",
        ) -> documents_models.DocumentTransactionModel | ErrorDetailsModel:
        """
        Add a file to a document upload transaction using bytes.

        Args:
            transaction_id (:obj:`str`): Document upload transaction ID.
            filename (:obj:`str`): File name.
            content_type (:obj:`str`): File mime-type
            file_bytes (:obj:`bytes`): File bytes.
            comment (:obj:`str`): Additional comment.
            relative_path (:obj:`str`): Relative path of the file inside the record.

        Returns:
            :obj:`pyil2.models.documents.DocumentTransactionModel`: Document upload transaction \
                status.
        """
        params = {
            "name": filename,
            "path": relative_path,
        }
        if comment:
            params['comment'] = comment
        resp = self._client.request(
            f'{self.base_url}/transaction/{transaction_id}',
            method='post',
            params=params,
            content_type=content_type,
            data=file_bytes,
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return documents_models.DocumentTransactionModel(**resp.json())

    def upload_document_file(
            self,
            transaction_id: str,
            filepath: str,
            comment: str = None,
            relative_path: str = "/",
            filename: str = None,
            content_type: str = None,
        ) -> documents_models.DocumentTransactionModel | ErrorDetailsModel:
        """
        Add a file to a document upload transaction using file path.
        This method will try to get the filename and the MIME-type from the filepath.
        If needed, you can force the filename and/or the content-type.

        Args:
            transaction_id (:obj:`str`): Document upload transaction ID.
            filepath (:obj:`str`): File path.
            comment (:obj:`str`): Additional comment.
            relative_path (:obj:`str`): Relative path of the file inside the record.
            filename (:obj:`str`): File name. \
                If None, it will try to use the filename in the filepath.
            content_type (:obj:`str`): File mime-type. \
                If None, it will try to guess the mime-type based on the file extension.

        Returns:
            :obj:`pyil2.models.documents.DocumentTransactionModel`: Document upload transaction \
                status.
        """
        if not filename:
            filename = os.path.basename(filepath)
        if not content_type:
            content_type = mimetypes.MimeTypes().guess_type(filepath)[0]

        params = {
            "name": filename,
            "path": relative_path,
        }
        if comment:
            params['comment'] = comment
        with open(filepath, 'rb') as f:
            resp = self._client.request(
                f'{self.base_url}/transaction/{transaction_id}',
                method='post',
                params=params,
                content_type=content_type,
                data=f,
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
        resp = self._client.request(
            f'{self.base_url}/transaction/{transaction_id}/commit',
            method='post',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return resp.json()

    def get_document_metadata(
            self,
            locator: str
        ) -> documents_models.DocumentMetadataModel | ErrorDetailsModel:
        """
        Get the documents metadata by the locator.

        Args:
            locator (:obj:`str`): Document locator.

        Returns:
            :obj:`pyil2.models.documents.DocumentMetadataModel`: Documents metadata.
        """
        resp = self._client.request(
            f'{self.base_url}/{locator}/metadata',
            method='get',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return documents_models.DocumentMetadataModel(**resp.json())

    def download_single_document_at(
            self,
            locator: str,
            index: int,
            dst_path: str = './',
        ) -> str | ErrorDetailsModel:
        """
        Download a single document by position from the set of documents 
        to a folder (default: current folder).

        Args:
            locator (:obj:`str`): A Documents Storage Locator.
            index (:obj:`int`): Index of the file.
            dst_path (:obj:`str`): Download the file to this folder.

        Returns:
            :obj:`str`: Downloaded file full path.
        """
        resp = self._client.download_file(
            f'{self.base_url}/{locator}/{index}',
            dst_path=dst_path
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return resp

    def download_documents_as_zip(
            self,
            locator: str,
            dst_path: str = './',
        ) -> str | ErrorDetailsModel:
        """
        Download documents in a compressed file to a folder (default: current folder).

        Args:
            locator (:obj:`str`): A Documents Storage Locator.
            dst_path (:obj:`str`): Download the file to this folder.

        Returns:
            :obj:`str`: Downloaded file full path.
        """
        resp = self._client.download_file(
            f'{self.base_url}/{locator}/zip',
            dst_path=dst_path
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return resp

    def download_single_document_at_as_response(
            self,
            locator: str,
            index: int,
        ) -> requests.Response | ErrorDetailsModel:
        """
        Get the request response to download a single document by position 
        from the set of documents.

        *Note:* For advance use only.

        Args:
            locator (:obj:`str`): A Documents Storage Locator.
            index (:obj:`int`): Index of the file.

        Returns:
            :obj:`requests.Response`: Request response.
        """
        resp = self._client.download_response(
            f'{self.base_url}/{locator}/{index}'
        )
        return resp

    def download_documents_as_zip_as_response(
            self,
            locator: str,
        ) -> requests.Response | ErrorDetailsModel:
        """
        Get the request response to download documents in a compressed file.

        *Note:* For advance use only.

        Args:
            locator (:obj:`str`): A Documents Storage Locator.

        Returns:
            :obj:`requests.Response`: Request response.
        """
        resp = self._client.download_response(
            f'{self.base_url}/{locator}/zip',
        )
        return resp
