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
from .base import BaseApiTest
from src.pyil2.models.base import ListModel
from src.pyil2.models import (
    chain as chain_models,
    errors,
    keys as keys_models,
    record as record_models,
)


class RecordApiTest(BaseApiTest):
    def setUp(self):
        super().setUp()
        self.api = self.client.api('record')

    def test_list_records(self):
        chains = self.api.list_records(self.default_chain)
        self.assertIsInstance(chains, ListModel)
        self.assertFalse(chains.last_to_first)
        for item in chains.items:
            self.assertIsInstance(item, record_models.RecordModel)
            self.assertIsInstance(item.payload_bytes, bytes)
        if chains.items:
            self.assertEqual(chains.items[0].serial, 0)

    def test_list_records_last_to_first(self):
        chains = self.api.list_records(self.default_chain, last_to_first=True)
        self.assertIsInstance(chains, ListModel)
        for item in chains.items:
            self.assertIsInstance(item, record_models.RecordModel)
        if chains.items:
            self.assertNotEqual(chains.items[0].serial, 0)
        self.assertTrue(chains.last_to_first)

    def test_list_records_page_params(self):
        chains = self.api.list_records(self.default_chain, page=1, size=1)
        self.assertIsInstance(chains, ListModel)
        for item in chains.items:
            self.assertIsInstance(item, record_models.RecordModel)
        if chains.items:
            self.assertNotEqual(chains.items[0].serial, 0)
        self.assertEqual(chains.page_size, 1)
        self.assertEqual(chains.page, 1)

    def test_list_records_first_serial(self):
        chains = self.api.list_records(self.default_chain, first_serial=1)
        self.assertIsInstance(chains, ListModel)
        for item in chains.items:
            self.assertIsInstance(item, record_models.RecordModel)
        if chains.items:
            self.assertEqual(chains.items[0].serial, 1)

    def test_list_records_last_serial(self):
        chains = self.api.list_records(
            self.default_chain, last_serial=1, last_to_first=True)
        self.assertIsInstance(chains, ListModel)
        for item in chains.items:
            self.assertIsInstance(item, record_models.RecordModel)
        if chains.items:
            self.assertEqual(chains.items[0].serial, 1)

    def test_list_records_ommit_payload(self):
        chains = self.api.list_records(self.default_chain, ommit_payload=True)
        self.assertIsInstance(chains, ListModel)
        for item in chains.items:
            self.assertIsInstance(item, record_models.RecordModel)
            self.assertIsNone(item.payload_bytes)

    def test_add_record(self):
        new_record = record_models.NewRecordModel(
            application_id=3,
            payload_bytes=b"+QFg+QQMBQEAKyMAAQAr+7WJlmPtPkXhG/cVa0JDs98aWrNnYQAyjMewRCGDwAoDCvkMLyf5A9r//yD5A9Qh+QLGI10FAwADASsjAAEAK/u1iZZj7T5F4Rv3FWtCQ7PfGlqzZ2EAMozHsEQhg8AKAwr5DC8K+QTmCgIK/QGOpUvmWysXBAAAyb+/rvRyv/mY40+xiIl9SLIB3NQK+5x9IMgl+BUAACj4EBD4CMVUIsoAPz6L3CEyqkqJYEzZ+s0wCCzgFL8Yc/E8yJGSO6t0ffP3L/Ko9zvLCEjDMBC/a/W/iU990r5a3geUwPz3AQT27PHIVc8Qca7+qlIn26cjRiklt1vTI8NHkuC0PCTy6MgNl7yzPz0TOliAs2ycTPOZaKBeDmrep0oY9yilLC6eKma7BapJC4Z91mNooYB89OrlB6pfMYoorkWoAgp+/I/+EUYFrJ3q8MxtPDWOerM0/bzgXh5j3SHh52DICtm4bcO5x2AHO/cIK632ioT+xhXW9m9rMS6abh1KfiKpKDC53j8ROx7ywx9ub1e+fyp9q6RX/3QV8KJJd5ZZ4Q0QAwEAAST5AVP4/PkBTgUBABX5AUcBLPkBQgUEABEcbWFpbm5ldC5jbGllbnRfbmFtZS5yZXN0LmFwaRQFBAIFCAErFwQAAMm/v670cr/5mONPsYiJfUiyAdzUKyMEAQBNyz0NsK6Mbkt9CK7TtRzz+krHR0uAj+310r901nGXCREAJfiVAAAo+JAQ+IiwGPGxkeNdus+DNzm7cnkd5J0+OkhPnrNbiE0kL9ftzMedJdGw5dCq7qVZNKl38gzVcM5ybQ9aIoygfl6wFYlSN43QjrAkEsPbaMb9su2uMQHV2bdWH3BCZq4/PiWuQe+VkhFho6dSYOiTJEwnSzpJN4CUF9AkXHIE213bjbmaEeHvfbF9t7TvAbG9ws0OeeVX9TEwPOToFvGIfodIQwlxGDzpkn5GdE8wxvmWcWZRKFTgLERjc41i33eIL9Svx2+O+B6b6qn+z3A95bHaumrYnR0hvf4njMDnMcSHAMuFWVXZOsjMepj53ydqrMIrXfe0A3lyE+STL7YnPC/02alIf6p9puKwdh2jdFG8ibIzBC7iE+OQige8BMShCY5fIRlq5YgxnnMqmlCkLPo0voQyZlgPjnsdpJ0J6Y8Agr1AcMmrZiUxf+UiHyxxDC3zRjyhHjAfTLBTwzH5hFE9bOWr2w1hU9HVIoM9+5oniMSXljBqtJPD79rs7IjEwFQQPv8QAwEAAQoBCgEUAQAVOQg4BQoBFAEAOAUKAhQBADgFCgMUAQA4BQoFFAEAOAUKBBQBADgFCggUAQA4BQoNFAEAOAUKZBQBACL4DwEAJvgKAAABa/m2PjpKDYsGVSxR28rUKJQuP+bnWugO1hnr9EbvDffzn60QKiL/4tA/6D+o2+Bd2GbRBR7qnxJEYochGY8zE9Qs8q0/SxWxtXSMhtQWVoGL5m5XzkXkxwrTPb5h9fB1X35Eo7JEgPGkIEWXJAjG2XPc6wfjWU0y5IpsCAT9RZewRsjb8TnDINA6efTMlvh0oQqLFy6WGIXDd8Sx2S12ygWcbiezADdD9iTRWBl7WpknZZePdWLyU720h/ukcWfrMWu/TYcJUWMajrnYfiQ6qvELqgaeE91CFatRZ02SG1THgXU/uB57l9Wyx5j0Ch8JexAuDCSKF1pSbobcw2WQ"
        )
        record = self.api.add_record(self.default_chain, new_record)
        self.assertIsInstance(record, record_models.RecordModel)

    def test_add_record_invalid_payload(self):
        new_record = record_models.NewRecordModel(
            application_id=3,
            payload_bytes=b"+QFg+QQMBQEVa0JDs98aWrNnYQAyjMewRCGDwAoDCvkMLyf5A9r//yD5A9Qh+QLGI10FAwADASsjAAEAK/u1iZZj7T5F4Rv3FWtCQ7PfGlqzZ2EAMozHsEQhg8AKAwr5DC8K+QTmCgIK/QGOpUvmWysXBAAAyb+/rvRyv/mY40+xiIl9SLIB3NQK+5x9IMgl+BUAACj4EBD4CMVUIsoAPz6L3CEyqkqJYEzZ+s0wCCzgFL8Yc/E8yJGSO6t0ffP3L/Ko9zvLCEjDMBC/a/W/iU990r5a3geUwPz3AQT27PHIVc8Qca7+qlIn26cjRiklt1vTI8NHkuC0PCTy6MgNl7yzPz0TOliAs2ycTPOZaKBeDmrep0oY9yilLC6eKma7BapJC4Z91mNooYB89OrlB6pfMYoorkWoAgp+/I/+EUYFrJ3q8MxtPDWOerM0/bzgXh5j3SHh52DICtm4bcO5x2AHO/cIK632ioT+xhXW9m9rMS6abh1KfiKpKDC53j8ROx7ywx9ub1e+fyp9q6RX/3QV8KJJd5ZZ4Q0QAwEAAST5AVP4/PkBTgUBABX5AUcBLPkBQgUEABEcbWFpbm5ldC5jbGllbnRfbmFtZS5yZXN0LmFwaRQFBAIFCAErFwQAAMm/v670cr/5mONPsYiJfUiyAdzUKyMEAQBNyz0NsK6Mbkt9CK7TtRzz+krHR0uAj+310r901nGXCREAJfiVAAAo+JAQ+IiwGPGxkeNdus+DNzm7cnkd5J0+OkhPnrNbiE0kL9ftzMedJdGw5dCq7qVZNKl38gzVcM5ybQ9aIoygfl6wFYlSN43QjrAkEsPbaMb9su2uMQHV2bdWH3BCZq4/PiWuQe+VkhFho6dSYOiTJEwnSzpJN4CUF9AkXHIE213bjbmaEeHvfbF9t7TvAbG9ws0OeeVX9TEwPOToFvGIfodIQwlxGDzpkn5GdE8wxvmWcWZRKFTgLERjc41i33eIL9Svx2+O+B6b6qn+z3A95bHaumrYnR0hvf4njMDnMcSHAMuFWVXZOsjMepj53ydqrMIrXfe0A3lyE+STL7YnPC/02alIf6p9puKwdh2jdFG8ibIzBC7iE+OQige8BMShCY5fIRlq5YgxnnMqmlCkLPo0voQyZlgPjnsdpJ0J6Y8Agr1AcMmrZiUxf+UiHyxxDC3zRjyhHjAfTLBTwzH5hFE9bOWr2w1hU9HVIoM9+5oniMSXljBqtJPD79rs7IjEwFQQPv8QAwEAAQoBCgEUAQAVOQg4BQoBFAEAOAUKAhQBADgFCgMUAQA4BQoFFAEAOAUKBBQBADgFCggUAQA4BQoNFAEAOAUKZBQBACL4DwEAJvgKAAABa/m2PjpKDYsGVSxR28rUKJQuP+bnWugO1hnr9EbvDffzn60QKiL/4tA/6D+o2+Bd2GbRBR7qnxJEYochGY8zE9Qs8q0/SxWxtXSMhtQWVoGL5m5XzkXkxwrTPb5h9fB1X35Eo7JEgPGkIEWXJAjG2XPc6wfjWU0y5IpsCAT9RZewRsjb8TnDINA6efTMlvh0oQqLFy6WGIXDd8Sx2S12ygWcbiezADdD9iTRWBl7WpknZZePdWLyU720h/ukcWfrMWu/TYcJUWMajrnYfiQ6qvELqgaeE91CFatRZ02SG1THgXU/uB57l9Wyx5j0Ch8JexAuDCSKF1pSbobcw2WQ"
        )
        record = self.api.add_record(self.default_chain, new_record)
        self.assertIsInstance(record, errors.ErrorDetailsModel)

    def test_get_record_at(self):
        record = self.api.get_record_at(self.default_chain, 0)
        self.assertIsInstance(record, record_models.RecordModel)
        self.assertEqual(record.serial, 0)

    def test_record_query(self):
        chains = self.api.query_records(
            self.default_chain, query="USE APP #3\nEVERYTHING")
        self.assertIsInstance(chains, ListModel)
        self.assertFalse(chains.last_to_first)
        for item in chains.items:
            self.assertIsInstance(item, record_models.RecordModel)
            self.assertIsInstance(item.payload_bytes, bytes)
            self.assertEqual(chains.items[0].application_id, 3)

    def test_record_query_how_many(self):
        chains = self.api.query_records(
            self.default_chain,
            query="USE APP #3\nEVERYTHING",
            how_many=1
        )
        self.assertIsInstance(chains, ListModel)
        self.assertFalse(chains.last_to_first)
        self.assertEqual(len(chains.items), 1)
        for item in chains.items:
            self.assertIsInstance(item, record_models.RecordModel)
            self.assertIsInstance(item.payload_bytes, bytes)
            self.assertEqual(chains.items[0].application_id, 3)

    def test_record_query_from_last_ommit(self):
        chains = self.api.query_records(
            self.default_chain,
            query="USE APP #3\nEVERYTHING",
            last_to_first=True,
            ommit_payload=True,
        )
        self.assertIsInstance(chains, ListModel)
        self.assertTrue(chains.last_to_first)
        for item in chains.items:
            self.assertIsInstance(item, record_models.RecordModel)
            self.assertIsNone(item.payload_bytes)
            self.assertEqual(chains.items[0].application_id, 3)
        if len(chains.items) > 1:
            self.assertGreater(chains.items[0].serial, chains.items[1].serial)

    def test_record_query_page(self):
        chains = self.api.query_records(
            self.default_chain,
            query="USE APP #3\nEVERYTHING",
            page=1,
            size=2
        )
        self.assertIsInstance(chains, ListModel)
        self.assertFalse(chains.last_to_first)
        self.assertLessEqual(len(chains.items), 2)
        self.assertEqual(chains.page, 1)

    def test_list_records_as_json(self):
        chains = self.api.list_records_as_json(self.default_chain)
        self.assertIsInstance(chains, ListModel)
        self.assertFalse(chains.last_to_first)
        for item in chains.items:
            self.assertIsInstance(item, record_models.RecordAsJsonModel)
            self.assertIsInstance(item.payload, dict)
        if chains.items:
            self.assertEqual(chains.items[0].serial, 0)

    def test_get_record_at_as_json(self):
        record = self.api.get_record_at_as_json(self.default_chain, 0)
        self.assertIsInstance(record, record_models.RecordAsJsonModel)
        self.assertEqual(record.serial, 0)

    def test_record_query_as_json(self):
        chains = self.api.query_records_as_json(
            self.default_chain, query="USE APP #3\nEVERYTHING")
        self.assertIsInstance(chains, ListModel)
        self.assertFalse(chains.last_to_first)
        for item in chains.items:
            self.assertIsInstance(item, record_models.RecordAsJsonModel)
            self.assertIsInstance(item.payload, dict)
            self.assertEqual(chains.items[0].application_id, 3)
