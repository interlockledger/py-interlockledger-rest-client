from .base import BaseApiTest
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
        self.certificate_2 = PKCS12Certificate(cert_2_filepath, cert_2_password)
        
    
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
        
        resp_from_get = self.api.get_json_document(self.default_chain, resp.serial)
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
        self.skipTest('TODO')
        payload = {
            'attr': 'value'
        }
        resp = self.api.add_json_document_with_chain_keys(
            self.default_chain,
            payload,
            self.second_chain,
        )
        self.assertIsInstance(resp, JsonDocumentModel)
        
    def test_get_json_document_invalid_serial(self):
        json_document = self.api.get_json_document(self.default_chain, 0)
        self.assertIsInstance(json_document, ErrorDetailsModel)
    
    def test_allow_reader_keys(self):
        data = {
            "contextId": "test_readers",
            "readers": [
                {
                    "name": "cert2",
                    "publicKey": self.certificate_2.pub_key
                }
            ]
        }
        allowed_readers = AllowedReadersModel(**data)
        reference = self.api.allow_json_document_readers(self.default_chain, allowed_readers)
        self.assertIsInstance(reference, str)

    def test_list_allowed_readers(self):
        allowed_readers = self.api.list_json_document_allowed_readers(
            self.default_chain
        )
        self.assertIsInstance(allowed_readers, ListModel)
        for item in allowed_readers.items:
            self.assertIsInstance(item, AllowedReadersDetailsModel)
            