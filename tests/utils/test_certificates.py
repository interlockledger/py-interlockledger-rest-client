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
import os
from unittest import TestCase
from src.pyil2.utils.certificates import PKCS12Certificate


class PKCS12CertificateTest(TestCase):
    def setUp(self) -> None:
        self.filepath = os.environ.get('TEST_CERTIFICATE_PATH')
        self.password = os.environ.get('TEST_CERTIFICATE_PASS')

        if not self.filepath or not self.password:
            self.skipTest(
                'Skipping TEST_CERTIFICATE_PATH or TEST_CERTIFICATE_PASS are not set as environment variables.')

    def test_default(self):
        # This test is only to see if it is openning correctly
        certificate = PKCS12Certificate(
            path=self.filepath, password=self.password)
        self.assertIsInstance(certificate.common_name, str)
        self.assertIsInstance(certificate.friendly_name, str)
        self.assertIsInstance(certificate.private_key, bytes)
        self.assertIsInstance(certificate.public_certificate, bytes)
        self.assertIsInstance(certificate.public_exponent, int)
        self.assertIsInstance(certificate.key_id, str)
        self.assertIsInstance(certificate.pub_key_hash, str)
        self.assertIsInstance(certificate.public_modulus, int)
