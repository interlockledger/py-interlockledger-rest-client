from .base import BaseApiTest
from src.pyil2.models import (
    chain as chain_models,
    records,
)

class ChainApiTest(BaseApiTest):
    def setUp(self):
        super().setUp()
        self.api = self.client.api('chain')
    
    def test_list_chains(self):
        chains = self.api.list_chains()
        self.assertIsInstance(chains, list)
        for item in chains:
            self.assertIsInstance(item, chain_models.ChainIdModel)

    def test_chain_summary(self):
        chain = self.api.summary(self.default_chain)
        self.assertIsInstance(chain, chain_models.ChainSummaryModel)
    
    def test_list_active_apps(self):
        apps = self.api.list_active_apps(self.default_chain)
        self.assertIsInstance(apps, list)
        for item in apps:
            self.assertIsInstance(item, int)

    def test_list_interlockings(self):
        interlocks = self.api.list_interlockings(self.default_chain)
        self.assertEqual(interlocks.page, 0)
        self.assertEqual(interlocks.page_size, 10)
        self.assertIsInstance(interlocks.items, list)
        for item in interlocks.items:
            self.assertIsInstance(item, records.InterlockingRecordModel)
        
    def test_list_interlockings_params(self):
        interlocks = self.api.list_interlockings(
                self.default_chain,
                page=1,
                size=2,
                how_many_from_last=5,                
            )
        self.assertEqual(interlocks.page, 1)
        self.assertEqual(interlocks.total_number_of_pages, 3)
        self.assertEqual(interlocks.page_size, 2)
        self.assertIsInstance(interlocks.items, list)
        for item in interlocks.items:
            self.assertIsInstance(item, records.InterlockingRecordModel)
        
    