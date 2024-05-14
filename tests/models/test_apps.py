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
from src.pyil2.utils.range import LimitedRange
from src.pyil2.models import apps
import datetime


class DataFieldEnumerationTest(TestCase):
    def test_from_string(self):
        value = '#1|name|description|'
        df_enum = apps.DataFieldEnumeration.from_concatenated_string(value)
        self.assertEqual(df_enum[0].id, 1)
        self.assertEqual(df_enum[0].name, 'name')
        self.assertEqual(df_enum[0].description, 'description')

    def test_from_string_no_final_pipe(self):
        value = '#1|name|description'
        df_enum = apps.DataFieldEnumeration.from_concatenated_string(value)
        self.assertEqual(df_enum[0].id, 1)
        self.assertEqual(df_enum[0].name, 'name')
        self.assertEqual(df_enum[0].description, 'description')

    def test_from_string_no_description(self):
        value = '#1|name|'
        df_enum = apps.DataFieldEnumeration.from_concatenated_string(value)
        self.assertEqual(df_enum[0].id, 1)
        self.assertEqual(df_enum[0].name, 'name')
        self.assertIsNone(df_enum[0].description)

    def test_from_string_no_description_no_final_pipe(self):
        value = '#1|name'
        df_enum = apps.DataFieldEnumeration.from_concatenated_string(value)
        self.assertEqual(df_enum[0].id, 1)
        self.assertEqual(df_enum[0].name, 'name')
        self.assertIsNone(df_enum[0].description)

    def test_from_string_no_description_empty_pipe(self):
        value = '#1|name||'
        df_enum = apps.DataFieldEnumeration.from_concatenated_string(value)
        self.assertEqual(df_enum[0].id, 1)
        self.assertEqual(df_enum[0].name, 'name')
        self.assertIsNone(df_enum[0].description)

    def test_from_list_string(self):
        value = '#1|name|description|#2|name2|description2|#3|name3|#4|name4#5|name5|description5|'
        df_enum = apps.DataFieldEnumeration.from_concatenated_string(value)
        expected = [
            (1, "name", "description"),
            (2, "name2", "description2"),
            (3, "name3", None),
            (4, "name4", None),
            (5, "name5", "description5"),
        ]
        for i in range(5):
            self.assertEqual(df_enum[i].id, expected[i][0])
            self.assertEqual(df_enum[i].name, expected[i][1])
            self.assertEqual(df_enum[i].description, expected[i][2])

    def test_to_string(self):
        df = apps.DataFieldEnumeration(
            id=1,
            name='name',
            description='description'
        )
        df_str = df.to_il2_string()
        self.assertEqual(df_str, '#1|name|description|')

    def test_to_string_no_description(self):
        df = apps.DataFieldEnumeration(
            id=1,
            name='name',
        )
        df_str = df.to_il2_string()
        self.assertEqual(df_str, '#1|name|')


class InterlockAppTraitsModelTest(TestCase):
    def test_from_dict(self):
        data = {
            "appVersion": "41.0.0.0",
            "dataModels": [
                {
                    "dataFields": [
                        {
                            "name": "Version",
                            "enumeration": "#0|AES256|AES256|#65535|None|In plaintext|",
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
        for model in app_trait.data_models:
            self.assertIsInstance(model, apps.DataModel)
            self.assertIsInstance(model.data_fields[0].enumeration, list)
            if model.data_fields[0].enumeration:
                self.assertIsInstance(
                    model.data_fields[0].enumeration[0], apps.DataFieldEnumeration)

        dump = app_trait.model_dump_json()
        self.assertIsInstance(dump, str)
        self.assertTrue(
            '"enumeration":"#0|AES256|AES256|#65535|None|In plaintext|"' in dump)
