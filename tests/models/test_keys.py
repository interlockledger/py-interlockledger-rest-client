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
from src.pyil2.enum import KeyPurpose
from src.pyil2.utils import AppPermissions
from src.pyil2.utils.certificates import PKCS12Certificate
from src.pyil2.models import keys
import datetime


class CertificatePermitModelTest(TestCase):
    def test_x509_bytes_as_str(self):
        data = {
            "name": "key name",
            "permissions": [
                "#2,500,501",
                "#1,300,301",
                "#5,701",
                "#3,601",
                "#4",
                "#8,2100"
            ],
            "purposes": [
                KeyPurpose.PROTOCOL,
                "Action",
                "KeyManagement"
            ],
            "certificateInX509": "certificate bytes"
        }
        model = keys.CertificatePermitModel(**data)
        self.assertEqual(model.name, data["name"])
        self.assertIsInstance(model.permissions, list)
        for item in model.permissions:
            self.assertIsInstance(item, AppPermissions)
        self.assertIsInstance(model.purposes, list)
        self.assertEqual(model.certificate_in_X509, "certificate bytes")

        dump = model.model_dump(exclude_none=True, by_alias=True)
        self.assertEqual(dump['name'], data['name'])
        self.assertIsInstance(dump['permissions'], list)
        for item in dump['permissions']:
            self.assertIsInstance(item, str)
        self.assertIsInstance(dump['purposes'], list)
        for item in dump['purposes']:
            self.assertIsInstance(item, str)
        self.assertEqual(dump['certificateInX509'], data['certificateInX509'])

    def test_x509_as_pkcs12(self):
        filepath = os.environ.get('TEST_CERTIFICATE_PATH')
        password = os.environ.get('TEST_CERTIFICATE_PASS')
        certificate = PKCS12Certificate(filepath, password)
        data = {
            "name": "key name",
            "permissions": [
                "#2,500,501",
                "#1,300,301",
                "#5,701",
                "#3,601",
                "#4",
                "#8,2100"
            ],
            "purposes": [
                KeyPurpose.PROTOCOL,
                "Action",
                "KeyManagement"
            ],
            "certificateInX509": certificate
        }
        model = keys.CertificatePermitModel(**data)
        self.assertEqual(model.name, data["name"])
        self.assertIsInstance(model.certificate_in_X509, str)

        dump = model.model_dump(exclude_none=True, by_alias=True)
        self.assertEqual(dump['name'], data['name'])
        self.assertIsInstance(dump['permissions'], list)
        for item in dump['permissions']:
            self.assertIsInstance(item, str)
        self.assertIsInstance(dump['purposes'], list)
        for item in dump['purposes']:
            self.assertIsInstance(item, str)
        self.assertIsInstance(dump['certificateInX509'], str)

    def test_permissions_as_instances(self):
        data = {
            "name": "key name",
            "permissions": [
                AppPermissions.resolve("#1,300,301")
            ],
            "purposes": [
                KeyPurpose.PROTOCOL,
                "Action",
                "KeyManagement"
            ],
            "certificateInX509": "certificate bytes"
        }
        model = keys.CertificatePermitModel(**data)
        self.assertEqual(model.name, data["name"])
        self.assertIsInstance(model.permissions, list)
        for item in model.permissions:
            self.assertIsInstance(item, AppPermissions)
        self.assertIsInstance(model.purposes, list)
        self.assertEqual(model.certificate_in_X509, "certificate bytes")

        dump = model.model_dump(exclude_none=True, by_alias=True)
        self.assertEqual(dump['name'], data['name'])
        self.assertIsInstance(dump['permissions'], list)
        for item in dump['permissions']:
            self.assertIsInstance(item, str)
        self.assertIsInstance(dump['purposes'], list)
        for item in dump['purposes']:
            self.assertIsInstance(item, str)
        self.assertEqual(dump['certificateInX509'], data['certificateInX509'])


class KeyDetailsModelTest(TestCase):
    def test_init_app_permission_from_string(self):
        key = keys.KeyDetailsModel(
            name='key.name',
            permissions=['#2,500,501'],
            purposes=['Action'],
            id='Key!id',
            public_key='PubKey!test'
        )
        self.assertIsInstance(key.permissions, list)
        for item in key.permissions:
            self.assertIsInstance(item, keys.AppPermissions)
