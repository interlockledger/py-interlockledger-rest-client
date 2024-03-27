import os
from unittest import TestCase
from src.pyil2.client import IL2Client

class IL2ClientTest(TestCase):
    def setUp(self) -> None:
        self.filepath = os.environ.get('TEST_CERTIFICATE_PATH')
        self.password = os.environ.get('TEST_CERTIFICATE_PASS')
        self.host = os.environ.get('TEST_HOST')

        if not self.filepath or not self.password or not self.host:
            self.skipTest('Skipping TEST_CERTIFICATE_PATH or TEST_CERTIFICATE_PASS or TEST_HOST are not set as environment variables.')
    
    def test_request_with_certificate(self):
        client = IL2Client(
            host=self.host,
            cert_filepath=self.filepath,
            cert_password=self.password,
            verify_ca=False,
        )
        resp = client._request('/', 'GET')
        self.assertEqual(resp.status_code, 200)
        
    
