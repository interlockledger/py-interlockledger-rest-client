# Copyright (c) 2024, InterlockLedger Network
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

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
import datetime
import os
from src.pyil2.models.base import ListModel
from src.pyil2.utils.certificates import PKCS12Certificate
from src.pyil2.models.errors import ErrorDetailsModel
from src.pyil2.models.json import (
    JsonDocumentModel,
    AllowedReadersModel,
    AllowedReadersDetailsModel
)


class JsonApiTest(BaseApiTest):
    def setUp(self):
        super().setUp()
        self.api = self.client.api('json')
        cert_2_filepath = os.environ.get('TEST_CERTIFICATE_2_PATH')
        cert_2_password = os.environ.get('TEST_CERTIFICATE_2_PASS')
        self.certificate = PKCS12Certificate(self.filepath, self.password)
        self.certificate_2 = PKCS12Certificate(
            cert_2_filepath, cert_2_password)

    def test_add_json_document(self):
        payload = {
            'attr': 'value'
        }
        resp = self.api.add_json_document(self.default_chain, payload)
        self.assertIsInstance(resp, JsonDocumentModel)
        decrypted = resp.encrypted_json.decode(self.certificate)
        self.assertDictEqual(decrypted, payload)
        with self.assertRaises(ValueError):
            decrypted = resp.encrypted_json.decode(self.certificate_2)

        resp_from_get = self.api.get_json_document(
            self.default_chain, resp.serial)
        self.assertIsInstance(resp_from_get, JsonDocumentModel)
        decrypted = resp_from_get.encrypted_json.decode(self.certificate)
        self.assertDictEqual(decrypted, payload)

    def test_add_json_with_key(self):
        payload = {
            'attr': 'value'
        }
        resp = self.api.add_json_document_with_key(
            self.default_chain,
            payload,
            self.certificate_2.pub_key,
            self.certificate_2.key_id
        )
        self.assertIsInstance(resp, JsonDocumentModel)
        decrypted = resp.encrypted_json.decode(self.certificate_2)
        self.assertDictEqual(decrypted, payload)

    def test_add_json_with_chain_key(self):
        context_id = f"test_readers_{int(datetime.datetime.now().timestamp())}"
        data = {
            "contextId": context_id,
            "readers": [
                {
                    "name": self.certificate_2.key_id,
                    "publicKey": self.certificate_2.pub_key
                }
            ]
        }
        allowed_readers = AllowedReadersModel(**data)
        reference = self.api.allow_json_document_readers(
            self.default_chain, allowed_readers)

        payload = {
            'attr': 'value'
        }
        resp = self.api.add_json_document_with_chain_keys(
            self.default_chain,
            payload,
            [self.default_chain],
        )
        self.assertIsInstance(resp, JsonDocumentModel)
        decrypted = resp.encrypted_json.decode(self.certificate_2)
        self.assertDictEqual(decrypted, payload)

    def test_add_json_with_indirect_key(self):
        context_id = f"test_readers_{int(datetime.datetime.now().timestamp())}"
        data = {
            "contextId": context_id,
            "readers": [
                {
                    "name": self.certificate_2.key_id,
                    "publicKey": self.certificate_2.pub_key
                }
            ]
        }
        allowed_readers = AllowedReadersModel(**data)
        reference = self.api.allow_json_document_readers(
            self.default_chain, allowed_readers)

        payload = {
            'attr': 'value'
        }
        resp = self.api.add_json_document_with_indirect_keys(
            self.default_chain,
            payload,
            [reference],
        )
        self.assertIsInstance(resp, JsonDocumentModel)
        decrypted = resp.encrypted_json.decode(self.certificate_2)
        self.assertDictEqual(decrypted, payload)

    def test_get_json_document_invalid_serial(self):
        json_document = self.api.get_json_document(self.default_chain, 0)
        self.assertIsInstance(json_document, ErrorDetailsModel)

    def test_allow_reader_keys(self):
        data = {
            "contextId": f"test_readers_{int(datetime.datetime.now().timestamp())}",
            "readers": [
                {
                    "name": self.certificate_2.key_id,
                    "publicKey": self.certificate_2.pub_key
                }
            ]
        }
        allowed_readers = AllowedReadersModel(**data)
        reference = self.api.allow_json_document_readers(
            self.default_chain, allowed_readers)
        self.assertIsInstance(reference, str)

    def test_list_allowed_readers(self):
        allowed_readers = self.api.list_json_document_allowed_readers(
            self.default_chain
        )
        self.assertIsInstance(allowed_readers, ListModel)
        for item in allowed_readers.items:
            self.assertIsInstance(item, AllowedReadersDetailsModel)
