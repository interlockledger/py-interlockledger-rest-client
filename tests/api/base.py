from unittest import TestCase
from src.pyil2.client import IL2Client
import os

class BaseApiTest(TestCase):
    def setUp(self):
        self.filepath = os.environ.get('TEST_CERTIFICATE_PATH')
        self.password = os.environ.get('TEST_CERTIFICATE_PASS')
        self.host = os.environ.get('TEST_HOST')

        if not self.filepath or not self.password or not self.host:
            self.skipTest('Skipping TEST_CERTIFICATE_PATH or TEST_CERTIFICATE_PASS or TEST_HOST are not set as environment variables.')
    
        self.client = IL2Client(
            host=self.host,
            cert_filepath=self.filepath,
            cert_password=self.password,
        )

    