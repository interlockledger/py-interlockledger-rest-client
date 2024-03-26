from .base import BaseApiTest
from src.pyil2.models import chain as chain_models

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
        