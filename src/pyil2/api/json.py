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
from typing import (
    Dict,
    Any,
    List,
)
from .base import BaseApi
from ..models.errors import ErrorDetailsModel
from ..models import json as json_models
from ..models.base import ListModel


class JsonApi(BaseApi):
    '''
    API class for the JSON documents requests.

    Args:
        client (:obj:`pyil2.IL2Client`): IL2Client to be used to send requests.

    Attributes:
        base_url (`str`): Base path of the requests.
    '''
    base_url = 'jsonDocuments@'

    def get_json_document(
            self,
            chain_id: str,
            serial: int
        ) -> json_models.JsonDocumentModel | ErrorDetailsModel:
        """
        Get a JSON document record by serial number.

        Args:
            chain_id (:obj:`str`): Chain ID.
            serial (`int`): Record serial number.

        Returns:
            :obj:`pyil2.models.json.JsonDocumentModel`: JSON document details.
        """
        resp = self._client.request(
            f'{self.base_url}{chain_id}/{serial}',
            method='get',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return json_models.JsonDocumentModel(**resp.json())

    def add_json_document(
            self,
            chain_id: str,
            payload: Dict[str, Any]
        ) -> json_models.JsonDocumentModel | ErrorDetailsModel:
        """
        Add a JSON document record encrypted with the client certificate used in the request.

        Args:
            chain_id (:obj:`str`): Chain ID.
            payload (:obj:`dict`): A valid JSON in dictionary format.

        Returns:
            :obj:`pyil2.models.json.JsonDocumentModel`: Added JSON document details.
        """
        resp = self._client.request(
            f'{self.base_url}{chain_id}',
            method='post',
            body=payload,
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return json_models.JsonDocumentModel(**resp.json())

    def add_json_document_with_key(
            self,
            chain_id: str,
            payload: Dict[str, Any],
            public_key: str,
            public_key_id: str
        ) -> json_models.JsonDocumentModel | ErrorDetailsModel:
        """
        Add a JSON document record encrypted with a given key.

        Args:
            chain_id (:obj:`str`): Chain ID.
            payload (:obj:`dict`): A valid JSON in dictionary format.
            public_key (:obj:`str`): IL2 text representation of a public key to \
                encrypt the content for.
            public_key_id (:obj:`str`): IL2 text representation of the key ID.

        Returns:
            :obj:`pyil2.models.json.JsonDocumentModel`: Added JSON document details.
        """
        headers = {
            'X-PubKey': public_key,
            'X-PubKeyId': public_key_id,
        }
        resp = self._client.request(
            f'{self.base_url}{chain_id}/withKey',
            method='post',
            body=payload,
            headers=headers
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return json_models.JsonDocumentModel(**resp.json())

    def add_json_document_with_indirect_keys(
            self,
            chain_id: str,
            payload: Dict[str, Any],
            keys_references: List[str],
        ) -> json_models.JsonDocumentModel | ErrorDetailsModel:
        """
        Add a JSON document record encrypted with the public keys from a given list of chains.

        Args:
            chain_id (:obj:`str`): Chain ID.
            payload (:obj:`dict`): A valid JSON in dictionary format.
            keys_references ([:obj:`str`]): List of references on the format 'chainId@serial' \
                to records on local chains containing 'allowed readers' lists.

        Returns:
            :obj:`pyil2.models.json.JsonDocumentModel`: Added JSON document details.
        """
        headers = {
            'X-PubKeyReferences': ','.join(keys_references),
        }
        resp = self._client.request(
            f'{self.base_url}{chain_id}/withIndirectKeys',
            method='post',
            body=payload,
            headers=headers
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return json_models.JsonDocumentModel(**resp.json())

    def add_json_document_with_chain_keys(
            self,
            chain_id: str,
            payload: Dict[str, Any],
            keys_chain_id: List[str],
        ) -> json_models.JsonDocumentModel | ErrorDetailsModel:
        """
        Add a JSON document record encrypted with the public keys from a given list of chains.

        Args:
            chain_id (:obj:`str`): Chain ID.
            payload (:obj:`dict`): A valid JSON in dictionary format.
            keys_chain_id ([:obj:`str`]): List of IDs of a local chain from which the \
                'allowed readers' list of public keys will be used to encrypt the content.

        Returns:
            :obj:`pyil2.models.json.JsonDocumentModel`: Added JSON document details.
        """
        headers = {
            'X-PubKeyChains': ','.join(keys_chain_id),
        }
        resp = self._client.request(
            f'{self.base_url}{chain_id}/withChainKeys',
            method='post',
            body=payload,
            headers=headers
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return json_models.JsonDocumentModel(**resp.json())

    def list_json_document_allowed_readers(
            self,
            chain_id: str,
            context_id: str = None,
            last_to_first: bool = False,
            page: int = 0,
            size: int = 10,
        ) -> ListModel[json_models.AllowedReadersDetailsModel] | ErrorDetailsModel:
        """
        Get a list of JSON document allowed reader keys.

        Args:
            chain_id (`str`): Chain ID.
            context_id (`str`): Filter by context ID name.
            last_to_first (`bool`): If `True`, return the items in reverse order.
            page (:obj:`int`): Page to return.
            size (:obj:`int`): Number of items per page.

        Returns:
            :obj:`pyil2.models.base.ListModel` \
                [:obj:`pyil2.models.json.AllowedReadersDetailsModel`]: \
                List of allowed reader keys.
        """
        params = {
            "page": page,
            "pageSize": size,
            "lastToFirst": last_to_first,
        }
        if context_id is not None:
            params['contextId'] = context_id

        resp = self._client.request(
            f'{self.base_url}{chain_id}/allow',
            method='get',
            params=params,
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return ListModel[json_models.AllowedReadersDetailsModel](**resp.json())

    def allow_json_document_readers(
            self,
            chain_id: str,
            allowed_readers: json_models.AllowedReadersModel
        ) -> str | ErrorDetailsModel:
        """
        Create a new list of allowed readers to encrypt JSON documents.

        Args:
            chain_id (:obj:`str`): Chain ID.
            allowed_readers (:obj:`pyil2.models.json.AllowedReadersModel`): \
                List of reader keys to be allowed.

        Returns:
            :obj:`str`: A record reference in the format chainId@recordSerial
        """
        resp = self._client.request(
            f'{self.base_url}{chain_id}/allow',
            method='post',
            body=allowed_readers.model_dump(by_alias=True, exclude_none=True),
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return resp.json()
