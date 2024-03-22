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
                KeyPurpose.Protocol,
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
                KeyPurpose.Protocol,
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
                KeyPurpose.Protocol,
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
        
    