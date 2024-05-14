# Copyright (c) 2024, InterlockLedger Network
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

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
from src.pyil2.models import chain
from src.pyil2.models import keys
from src.pyil2.utils.certificates import PKCS12Certificate
import datetime


class ChainIdModelTest(TestCase):
    def test_base(self):
        data = {
            "id": "chain_id",
            "lastRecord": 40,
            "lastUpdate": "2023-10-17T21:00:02.015+00:00",
            "sizeInBytes": 74153,
        }
        model = chain.ChainIdModel(**data)
        self.assertFalse(model.closed)

    def test_closed_for_transaction(self):
        data = {
            "id": "chain_id",
            "lastRecord": 40,
            "lastUpdate": "2023-10-17T21:00:02.015+00:00",
            "licensingStatus": "Perpetually licensed",
            "name": "Chain name",
            "sizeInBytes": 74153,
            "isClosedForNewTransactions": False,
        }
        model = chain.ChainIdModel(**data)
        self.assertFalse(model.closed)
        data["isClosedForNewTransactions"] = True
        model = chain.ChainIdModel(**data)
        self.assertTrue(model.closed)


class ChainCreationModelTest(TestCase):
    def setUp(self) -> None:
        self.data = {
            "name": "Chain Name",
            "emergencyClosingKeyPassword": "emergency_password",
            "managementKeyPassword": "management_password",
        }

    def test_base(self):
        model = chain.ChainCreationModel(**self.data)
        self.assertEqual(model.name, self.data['name'])
        self.assertEqual(model.emergency_closing_key_password,
                         self.data['emergencyClosingKeyPassword'])
        self.assertEqual(model.management_key_password,
                         self.data['managementKeyPassword'])

        dump = model.model_dump(by_alias=True, exclude_none=True)
        self.assertEqual(dump['name'], self.data['name'])
        self.assertEqual(dump['emergencyClosingKeyPassword'],
                         self.data['emergencyClosingKeyPassword'])
        self.assertEqual(dump['managementKeyPassword'],
                         self.data['managementKeyPassword'])
        self.assertEqual(dump['emergencyClosingKeyStrength'], 'ExtraStrong')
        self.assertEqual(dump['managementKeyStrength'], 'Strong')

    def test_certificate(self):
        filepath = os.environ.get('TEST_CERTIFICATE_PATH')
        password = os.environ.get('TEST_CERTIFICATE_PASS')
        certificate = PKCS12Certificate(filepath, password)
        self.data['apiCertificates'] = [
            keys.CertificatePermitModel(
                name="Name",
                permissions=["#4"],
                purposes=["Action"],
                certificate_in_X509=certificate
            )
        ]
        model = chain.ChainCreationModel(**self.data)
        self.assertIsInstance(model, chain.ChainCreationModel)
        dump = model.model_dump(by_alias=True, exclude_none=True)
        self.assertIsInstance(dump['apiCertificates'], list)
        self.assertEqual(len(dump['apiCertificates']), 1)
        self.assertIsInstance(dump['apiCertificates'][0]['name'], str)
        self.assertIsInstance(dump['apiCertificates'][0]['permissions'], list)
        self.assertIsInstance(dump['apiCertificates']
                              [0]['permissions'][0], str)
        self.assertIsInstance(dump['apiCertificates'][0]['purposes'], list)
        self.assertIsInstance(dump['apiCertificates'][0]['purposes'][0], str)
        self.assertIsInstance(dump['apiCertificates']
                              [0]['certificateInX509'], str)
