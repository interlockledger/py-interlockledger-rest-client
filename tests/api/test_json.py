from .base import BaseApiTest
from src.pyil2.utils.certificates import PKCS12Certificate
from src.pyil2.models.errors import ErrorDetailsModel
from src.pyil2.models.json import JsonDocumentModel

class JsonApiTest(BaseApiTest):
    def setUp(self):
        super().setUp()
        self.api = self.client.api('json')
        self.certificate = PKCS12Certificate(self.filepath, self.password)
        
    
    def test_add_json_document(self):
        payload = {
            'attr': 'value'
        }
        resp = self.api.add_json_document(self.default_chain, payload)
        self.assertIsInstance(resp, JsonDocumentModel)
        decrypted = resp.encrypted_json.decode(self.certificate)
        self.assertDictEqual(decrypted, payload)
