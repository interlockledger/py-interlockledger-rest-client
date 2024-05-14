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
from typing import List
from .base import BaseApi
from ..models.errors import ErrorDetailsModel
from ..models.base import ListModel
from ..models.record import OpaqueRecordModel


class OpaqueApi(BaseApi):
    '''
    API class for the opaque requests.

    Args:
        client (:obj:`pyil2.IL2Client`): IL2Client to be used to send requests.

    Attributes:
        base_url (`str`): Base path of the requests.
    '''
    base_url = 'opaque/'

    def add_opaque(
            self,
            chain_id: str,
            application_id: int,
            payload_type_id: int,
            payload: bytes,
            last_changed_serial: int = None,
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
            last_changed_serial (:obj:`int`): The serial number that the last record \
                in the chain must be equal.

        Returns:
            :obj:`pyil2.models.record.OpaqueRecordModel`: Opaque record details.
        """
        params = {
            "appId": application_id,
            "payloadTypeId": payload_type_id,
        }
        if last_changed_serial is not None:
            params['lastChangedRecordSerial'] = last_changed_serial

        resp = self._client.request(
            f'{self.base_url}{chain_id}',
            method='post',
            content_type='application/octet-stream',
            data=payload,
            params=params
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return OpaqueRecordModel(**resp.json())

    def get_opaque(
            self,
            chain_id: str,
            serial: int
        ) -> OpaqueRecordModel | ErrorDetailsModel:
        """
        Get an opaque record in a chain by serial number.

        Args:
            chain_id (`str`): Chain ID.
            serial (`int`): Record serial number.

        Returns:
            :obj:`pyil2.models.record.OpaqueRecordModel`: Opaque record details.
        """
        resp = self._client.request(
            f'{self.base_url}{chain_id}@{serial}',
            method='get',
            accept='application/octet-stream',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        model = OpaqueRecordModel(
            chain_id=chain_id,
            serial=serial,
            application_id=resp.headers.get('x-app-id'),
            payload_type_id=resp.headers.get('x-payload-type-id'),
            payload_length=len(resp.content),
            created_at=resp.headers.get('x-created-at'),
            payload=resp.content,
        )
        return model

    def query_opaque(
            self,
            chain_id: str,
            application_id: int,
            payload_type_ids: List[int] = None,
            how_many: int = None,
            last_to_first: bool = False,
            page: int = 0,
            size: int = 10,
        ) -> ListModel[OpaqueRecordModel] | ErrorDetailsModel:
        """
        Query opaque records in a chain.

        Args:
            chain_id (`str`): Chain ID.
            application_id (`int`): Application ID which records will be queried.
            payload_type_ids ([`int`]): List of opaque payload type IDs.
            how_many (`int`): How many records to return. If ommited or 0 returns all.
            last_to_first (`bool`): If `True`, return the items in reverse order.
            page (:obj:`int`): Page to return.
            size (:obj:`int`): Number of items per page.

        Returns:
            :obj:`pyil2.models.base.ListModel` \
                [:obj:`pyil2.models.record.OpaqueRecordModel`]: \
                List of opaque records in a chain.
        """
        params = {
            "appId": application_id,
            "page": page,
            "pageSize": size,
            "lastToFirst": last_to_first,
        }
        if payload_type_ids:
            params['payloadTypeIds'] = payload_type_ids
        if how_many is not None:
            params['howMany'] = how_many

        resp = self._client.request(
            url=f'{self.base_url}{chain_id}/asJson/query',
            method='get',
            params=params,
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return ListModel[OpaqueRecordModel](**resp.json())
