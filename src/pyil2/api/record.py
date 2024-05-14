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
from ..models.base import ListModel
from ..models.errors import ErrorDetailsModel
from ..models import record as record_models

from .base import BaseApi


class RecordApi(BaseApi):
    '''
    API class for the record requests.

    Args:
        client (:obj:`pyil2.IL2Client`): IL2Client to be used to send requests.

    Attributes:
        base_url (`str`): Base path of the requests.
    '''

    base_url = 'records@'

    def list_records(
            self,
            chain_id: str,
            first_serial: int = None,
            last_serial: int = None,
            last_to_first: bool = False,
            ommit_payload: bool = False,
            page: int = 0,
            size: int = 10,
        ) -> ListModel[record_models.RecordModel] | ErrorDetailsModel:
        """
        Get a list of records in a chain.

        Args:
            chain_id (`str`): Chain ID.
            first_serial (`int`): Serial number of first record to read. \
                Default: First in whole chain.
            last_serial (`int`): Serial number of last record to read. \
                Default: Last in whole chain.
            last_to_first (`bool`): If `True`, return the items in reverse order.
            ommit_payload (`bool`): If `True`, ommits the payload in the response.
            page (:obj:`int`): Page to return.
            size (:obj:`int`): Number of items per page.

        Returns:
            :obj:`pyil2.models.base.ListModel` \
                [:obj:`pyil2.models.record.RecordModel`]: List of records in a chain.
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

        resp = self._client.request(
            url=f'{self.base_url}{chain_id}',
            method='get',
            params=params,
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return ListModel[record_models.RecordModel](**resp.json())

    def add_record(
            self,
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
            new_record (:obj:`pyil2.models.record.NewRecordModel`): \
                Model with the description of the new record.

        Returns:
            :obj:`pyil2.models.record.RecordModel`: Added record model.
        """
        if not isinstance(new_record, record_models.NewRecordModel):
            raise ValueError("'new_record' must be a NewRecordModel.")
        resp = self._client.request(
            url=f'{self.base_url}{chain_id}',
            method='post',
            body=new_record.model_dump(exclude_none=True, by_alias=True)
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return record_models.RecordModel(**resp.json())

    def get_record_at(
            self,
            chain_id: str,
            serial: int,
        ) -> record_models.RecordModel | ErrorDetailsModel:
        """
        Get a record by serial number.

        Args:
            chain_id (`str`): Chain ID.
            serial (`int`): Record serial number.

        Returns:
            :obj:`pyil2.models.record.RecordModel`: Record in a chain.
        """
        resp = self._client.request(
            url=f'{self.base_url}{chain_id}/{serial}',
            method='get',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return record_models.RecordModel(**resp.json())

    def query_records(
            self,
            chain_id: str,
            query: str,
            how_many: int = None,
            last_to_first: bool = False,
            ommit_payload: bool = False,
            page: int = 0,
            size: int = 10,
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
            :obj:`pyil2.models.base.ListModel` \
                [:obj:`pyil2.models.record.RecordModel`]: List of records in a chain.
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

        resp = self._client.request(
            url=f'{self.base_url}{chain_id}/query',
            method='get',
            params=params,
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return ListModel[record_models.RecordModel](**resp.json())

    def list_records_as_json(
            self,
            chain_id: str,
            first_serial: int = None,
            last_serial: int = None,
            last_to_first: bool = False,
            page: int = 0,
            size: int = 10,
        ) -> ListModel[record_models.RecordAsJsonModel] | ErrorDetailsModel:
        """
        Get a list of records in a chain with the payload mapped to a JSON format.

        Args:
            chain_id (`str`): Chain ID.
            first_serial (`int`): Serial number of first record to read. \
                Default: First in whole chain.
            last_serial (`int`): Serial number of last record to read. Default: Last in whole chain.
            last_to_first (`bool`): If `True`, return the items in reverse order.
            page (:obj:`int`): Page to return.
            size (:obj:`int`): Number of items per page.

        Returns:
            :obj:`pyil2.models.base.ListModel` \
                [:obj:`pyil2.models.record.RecordAsJsonModel`]: \
                List of records in a chain with the payload as JSON.
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

        resp = self._client.request(
            url=f'{self.base_url}{chain_id}/asJson',
            method='get',
            params=params,
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return ListModel[record_models.RecordAsJsonModel](**resp.json())

    def get_record_at_as_json(
            self,
            chain_id: str,
            serial: int,
        ) -> record_models.RecordAsJsonModel | ErrorDetailsModel:
        """
        Get a record with the payload as JSON by serial number.

        Args:
            chain_id (`str`): Chain ID.
            serial (`int`): Record serial number.

        Returns:
            :obj:`pyil2.models.record.RecordAsJsonModel`: \
                Record in a chain with the payload as JSON.
        """
        resp = self._client.request(
            url=f'{self.base_url}{chain_id}/asJson/{serial}',
            method='get',
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return record_models.RecordAsJsonModel(**resp.json())

    def query_records_as_json(
            self,
            chain_id: str,
            query: str,
            how_many: int = None,
            last_to_first: bool = False,
            page: int = 0,
            size: int = 10,
        ) -> ListModel[record_models.RecordAsJsonModel] | ErrorDetailsModel:
        """
        Query records with the payload as JSON in a chain using the InterlockQL language.

        Args:
            chain_id (`str`): Chain ID.
            query (`str`): Query in the InterlockQL language.
            how_many (`int`): How many records to return. If ommited or 0 returns all.
            last_to_first (`bool`): If `True`, return the items in reverse order.
            page (:obj:`int`): Page to return.
            size (:obj:`int`): Number of items per page.

        Returns:
            :obj:`pyil2.models.base.ListModel` \
                [:obj:`pyil2.models.record.RecordAsJsonModel`]: \
                List of records in a chain with the payload as JSON.
        """
        params = {
            "queryAsInterlockQL": query,
            "page": page,
            "pageSize": size,
            "lastToFirst": last_to_first,
        }
        if how_many is not None:
            params['howMany'] = how_many

        resp = self._client.request(
            url=f'{self.base_url}{chain_id}/asJson/query',
            method='get',
            params=params,
        )
        if isinstance(resp, ErrorDetailsModel):
            return resp
        return ListModel[record_models.RecordAsJsonModel](**resp.json())
