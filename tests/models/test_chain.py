import os
from unittest import TestCase
from src.pyil2.models import chain
from src.pyil2.models import keys
from src.pyil2.utils.certificates import PKCS12Certificate
import datetime

class ChainIdModelTest(TestCase):
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
        self.assertEqual(model.emergency_closing_key_password, self.data['emergencyClosingKeyPassword'])
        self.assertEqual(model.management_key_password, self.data['managementKeyPassword'])

        dump = model.model_dump(by_alias=True, exclude_none=True)
        self.assertEqual(dump['name'], self.data['name'])
        self.assertEqual(dump['emergencyClosingKeyPassword'], self.data['emergencyClosingKeyPassword'])
        self.assertEqual(dump['managementKeyPassword'], self.data['managementKeyPassword'])
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
        self.assertIsInstance(dump['apiCertificates'][0]['permissions'][0], str)
        self.assertIsInstance(dump['apiCertificates'][0]['purposes'], list)
        self.assertIsInstance(dump['apiCertificates'][0]['purposes'][0], str)
        self.assertIsInstance(dump['apiCertificates'][0]['certificateInX509'], str)
        
