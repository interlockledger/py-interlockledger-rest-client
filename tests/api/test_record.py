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
        chains = self.api.list_records(self.default_chain, last_serial=1, last_to_first=True)
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