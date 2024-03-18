import os
from unittest import TestCase
from src.pyil2.utils.certificates import PKCS12Certificate


class PKCS12CertificateTest(TestCase):
    def setUp(self) -> None:
        self.filepath = os.environ.get('TEST_CERTIFICATE_PATH')
        self.password = os.environ.get('TEST_CERTIFICATE_PASS')

        if not self.filepath or not self.password:
            self.skipTest('Skipping TEST_CERTIFICATE_PATH or TEST_CERTIFICATE_PASS are not set as environment variables.')

    def test_default(self):
        # This test is only to see if it is openning correctly
        certificate = PKCS12Certificate(path=self.filepath, password=self.password)
        self.assertIsInstance(certificate.common_name, str)
        self.assertIsInstance(certificate.friendly_name, str)
        self.assertIsInstance(certificate.private_key, bytes)
        self.assertIsInstance(certificate.public_certificate, bytes)
        self.assertIsInstance(certificate.public_exponent, int)
        self.assertIsInstance(certificate.key_id, str)
        self.assertIsInstance(certificate.pub_key_hash, str)
        self.assertIsInstance(certificate.public_modulus, int)
        