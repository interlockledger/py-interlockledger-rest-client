from unittest import TestCase
import os
from src.pyil2.models import json as json_models
from src.pyil2.utils.certificates import PKCS12Certificate


class ReadingKeyModelTest(TestCase):
    def setUp(self):
        self.encrypted_iv = os.environ.get("TEST_CERTIFICATE_ENCRYPTED_IV")
        self.encrypted_key = os.environ.get("TEST_CERTIFICATE_ENCRYPTED_KEY")
        self.public_key_hash = os.environ.get("TEST_CERTIFICATE_PUBLIC_KEY_HASH")
        self.reader_id = os.environ.get("TEST_CERTIFICATE_READER_ID")
        
        self.cert_filepath = os.environ.get('TEST_CERTIFICATE_PATH')
        self.cert_password = os.environ.get('TEST_CERTIFICATE_PASS')

        self.cert_2_filepath = os.environ.get('TEST_CERTIFICATE_2_PATH')
        self.cert_2_password = os.environ.get('TEST_CERTIFICATE_2_PASS')
    
    def test_from_camel(self):
        data = {
            "encryptedIV": self.encrypted_iv,
            "encryptedKey": self.encrypted_key,
            "publicKeyHash": self.public_key_hash,
            "readerId": self.reader_id
        }
        reading_key = json_models.ReadingKeyModel(**data)
        self.assertEqual(reading_key.encrypted_iv, data['encryptedIV'])
        self.assertEqual(reading_key.encrypted_key, data['encryptedKey'])
        self.assertEqual(reading_key.public_key_hash, data['publicKeyHash'])
        self.assertEqual(reading_key.reader_id, data['readerId'])

    def test_check_certificate(self):
        reading_key = json_models.ReadingKeyModel(
            encrypted_iv=self.encrypted_iv,
            encrypted_key=self.encrypted_key,
            public_key_hash=self.public_key_hash,
            reader_id=self.reader_id,
        )
        certificate = PKCS12Certificate(self.cert_2_filepath, self.cert_2_password)
        self.assertFalse(reading_key.check_certificate(certificate))