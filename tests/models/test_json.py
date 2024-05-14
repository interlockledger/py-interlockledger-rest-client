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
from unittest import TestCase
import os
from src.pyil2.models import json as json_models
from src.pyil2.utils.certificates import PKCS12Certificate


class BaseEncryptedTest(TestCase):
    def setUp(self):
        self.encrypted_iv = os.environ.get("TEST_CERTIFICATE_ENCRYPTED_IV")
        self.encrypted_key = os.environ.get("TEST_CERTIFICATE_ENCRYPTED_KEY")
        self.public_key_hash = os.environ.get(
            "TEST_CERTIFICATE_PUBLIC_KEY_HASH")
        self.reader_id = os.environ.get("TEST_CERTIFICATE_READER_ID")

        self.cert_filepath = os.environ.get('TEST_CERTIFICATE_PATH')
        self.cert_password = os.environ.get('TEST_CERTIFICATE_PASS')

        self.cert_2_filepath = os.environ.get('TEST_CERTIFICATE_2_PATH')
        self.cert_2_password = os.environ.get('TEST_CERTIFICATE_2_PASS')

        self.cipher_text = os.environ.get('TEST_CIPHER_TEXT')


class ReadingKeyModelTest(BaseEncryptedTest):
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
        certificate = PKCS12Certificate(self.cert_filepath, self.cert_password)
        self.assertTrue(reading_key.check_certificate(certificate))

    def test_check_certificate_invalid(self):
        reading_key = json_models.ReadingKeyModel(
            encrypted_iv=self.encrypted_iv,
            encrypted_key=self.encrypted_key,
            public_key_hash=self.public_key_hash,
            reader_id=self.reader_id,
        )
        certificate = PKCS12Certificate(
            self.cert_2_filepath, self.cert_2_password)
        self.assertFalse(reading_key.check_certificate(certificate))


class EncryptedTextModelTest(BaseEncryptedTest):
    def test_decode(self):
        data = {
            "cipher": "AES256",
            "cipherText": self.cipher_text,
            "readingKeys": [
                {
                    "encryptedIV": self.encrypted_iv,
                    "encryptedKey": self.encrypted_key,
                    "publicKeyHash": self.public_key_hash,
                    "readerId": self.reader_id
                }
            ]
        }
        encrypted_text = json_models.EncryptedTextModel(**data)
        certificate = PKCS12Certificate(self.cert_filepath, self.cert_password)

        decrypted = encrypted_text.decode(certificate)
        self.assertIsInstance(decrypted, dict)

    def test_decode_invalid_certificate(self):
        data = {
            "cipher": "AES256",
            "cipherText": self.cipher_text,
            "readingKeys": [
                {
                    "encryptedIV": self.encrypted_iv,
                    "encryptedKey": self.encrypted_key,
                    "publicKeyHash": self.public_key_hash,
                    "readerId": self.reader_id
                }
            ]
        }
        encrypted_text = json_models.EncryptedTextModel(**data)
        certificate = PKCS12Certificate(
            self.cert_2_filepath, self.cert_2_password)

        with self.assertRaises(ValueError):
            decrypted = encrypted_text.decode(certificate)
