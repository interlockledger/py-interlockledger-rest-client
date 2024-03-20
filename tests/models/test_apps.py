from unittest import TestCase
from src.pyil2.utils.range import LimitedRange
from src.pyil2.models import apps
import datetime

class InterlockAppTraitsModelTest(TestCase):
    def test_from_dict(self):
        data = {
            "appVersion": "41.0.0.0",
            "dataModels": [
                {
                "dataFields": [
                    {
                    "name": "Version",
                    "subDataFields": [
                        {
                            "name": "Version",
                            "subDataFields": [],
                            "tagId": 5,
                            "version": 1,
                        },
                    ],
                    "tagId": 5,
                    "version": 1,
                    },
                ],
                "indexes": [
                    {
                    "elements": [
                        {
                        "fieldPath": "IssuerName"
                        }
                    ],
                    "isUnique": True,
                    "name": "IssuerName"
                    }
                ],
                "payloadName": "ProofOfOwnership",
                "payloadTagId": 1102,
                "version": 2
                },
            ],
            "description": "Description text",
            "id": 100,
            "name": "Asset Management",
            "publisherId": "Key!Id",
            "publisherName": "InterlockLedgerCore",
            "reservedILTagIds": [
                "[1100-1999]"
            ],
            "start": "2023-10-17T20:59:10.8+00:00",
            "version": 1
        }

        app_trait = apps.InterlockAppTraitsModel(**data)
        self.assertIsInstance(app_trait.app_version, str)
        self.assertIsInstance(app_trait.description, str)
        self.assertIsInstance(app_trait.id, int)
        self.assertIsInstance(app_trait.name, str)
        self.assertIsInstance(app_trait.publisher_id, str)
        self.assertIsInstance(app_trait.publisher_name, str)
        self.assertIsInstance(app_trait.start, datetime.datetime)
        self.assertIsInstance(app_trait.version, int)
        
        self.assertIsInstance(app_trait.reserved_il_tag_ids, list)
        for tag in app_trait.reserved_il_tag_ids:
            self.assertIsInstance(tag, LimitedRange)
        
        self.assertIsInstance(app_trait.data_models, list)
        for tag in app_trait.data_models:
            self.assertIsInstance(tag, apps.DataModel)
        
            
        dump = app_trait.model_dump_json()
        self.assertIsInstance(dump, str)