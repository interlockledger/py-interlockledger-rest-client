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
from .base import BaseApiTest
from src.pyil2.models.base import ListModel
from src.pyil2.models.errors import ErrorDetailsModel
from src.pyil2.models.record import OpaqueRecordModel


class OpaqueApiTest(BaseApiTest):
    def setUp(self):
        super().setUp()
        self.api = self.client.api('opaque')

    def test_opaque(self):
        opaque = self.api.add_opaque(
            chain_id=self.default_chain,
            application_id=13,
            payload_type_id=1313,
            payload=b'test2'
        )
        self.assertIsInstance(opaque, OpaqueRecordModel)

        resp = self.api.get_opaque(self.default_chain, opaque.serial)
        self.assertEqual(opaque.serial, resp.serial)
        self.assertEqual(opaque.application_id, resp.application_id)
        self.assertEqual(opaque.payload_type_id, resp.payload_type_id)
        self.assertEqual(opaque.created_at.replace(
            microsecond=0), resp.created_at.replace(microsecond=0))
        self.assertEqual(resp.payload, b'test2')

    def test_opaque_last_changed_serial_error(self):
        opaque = self.api.add_opaque(
            chain_id=self.default_chain,
            application_id=13,
            payload_type_id=1313,
            payload=b'test',
            last_changed_serial=0
        )
        self.assertIsInstance(opaque, ErrorDetailsModel)

    def test_get_opaque_invalid_serial(self):
        opaque = self.api.get_opaque(self.default_chain, 0)
        self.assertIsInstance(opaque, ErrorDetailsModel)

    def test_query_opaque(self):
        opaques = self.api.query_opaque(
            self.default_chain,
            application_id=13
        )
        self.assertIsInstance(opaques, ListModel)
        for item in opaques.items:
            self.assertIsInstance(item, OpaqueRecordModel)

    def test_query_opaque_filter_type_ids(self):
        opaque = self.api.add_opaque(
            chain_id=self.default_chain,
            application_id=13,
            payload_type_id=1313,
            payload=b'test2'
        )
        opaque = self.api.add_opaque(
            chain_id=self.default_chain,
            application_id=13,
            payload_type_id=131313,
            payload=b'test2'
        )

        opaques = self.api.query_opaque(
            self.default_chain,
            application_id=13,
            payload_type_ids=[1313],
            last_to_first=True
        )
        self.assertIsInstance(opaques, ListModel)
        for item in opaques.items:
            self.assertIsInstance(item, OpaqueRecordModel)
            self.assertEqual(item.payload_type_id, 1313)

    def test_query_opaque_filter_empty_type_ids(self):
        opaques = self.api.query_opaque(
            self.default_chain,
            application_id=13,
            payload_type_ids=[1414],
            last_to_first=True
        )
        self.assertIsInstance(opaques, ListModel)
        self.assertEqual(len(opaques.items), 0)

    def test_query_opaque_filter_empty_app_id(self):
        opaques = self.api.query_opaque(
            self.default_chain,
            application_id=131313,
        )
        self.assertIsInstance(opaques, ListModel)
        self.assertEqual(len(opaques.items), 0)
