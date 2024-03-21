from unittest import TestCase
from src.pyil2.client import IL2Client
import os

class BaseApiTest(TestCase):
    def setUp(self):
        self.filepath = os.environ.get('TEST_CERTIFICATE_PATH')
        self.password = os.environ.get('TEST_CERTIFICATE_PASS')
        self.host = os.environ.get('TEST_HOST')
        self.default_chain = os.environ.get('TEST_DEFAULT_CHAIN')

        if not self.filepath or not self.password or not self.host or not self.default_chain:
            self.skipTest('Skipping TEST_CERTIFICATE_PATH or TEST_CERTIFICATE_PASS or TEST_HOST or TEST_DEFAULT_CHAIN are not set as environment variables.')
    
        self.client = IL2Client(
            host=self.host,
            cert_filepath=self.filepath,
            cert_password=self.password,
            timeout=100
        )

    