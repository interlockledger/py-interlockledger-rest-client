from unittest import TestCase
import os
from src.pyil2 import IL2Client


class TASDASD(TestCase):
    
    def setUp(self) -> None:
        self.filepath = os.environ.get('TEST_CERTIFICATE_PATH')
        self.password = os.environ.get('TEST_CERTIFICATE_PASS')
        self.host = os.environ.get('TEST_HOST')

    def test_sample(self):
        client = IL2Client(
            host=self.host,
            cert_filepath=self.filepath,
            cert_password=self.password,
            verify_ca=False,
        )
        chain_api = client.api('chain')
        chains = chain_api.list_chains()
        chain_id = chains[0].id
        
        json_api = client.api('json')
        encrypted_json = json_api.add_json_document(
            chain_id,
            {
                'attribute': "value"
            }
        )
        pass