from .base import BaseApiTest
from src.pyil2.models import (
    node,
    apps as apps_models,
    records,
    chains,
)

class NodeApiTest(BaseApiTest):
    def setUp(self):
        super().setUp()
        self.api = self.client.api('node')
    
    def test_details(self):
        details = self.api.details
        self.assertIsInstance(details.id, str)
        self.assertIsInstance(details.name, str)
        self.assertIsInstance(details.network, str)
        self.assertIsInstance(details.owner_id, str)
        self.assertIsInstance(details.owner_name, str)
        self.assertIsInstance(details.peer_address, str)
        self.assertIsInstance(details.color, str)
        self.assertIsInstance(details.chains, list)
        self.assertIsInstance(details.extensions, dict)
        self.assertIsInstance(details.software_versions, node.SoftwerVersionModel)
    
    def test_peers(self):
        peers = self.api.list_peers()
        self.assertIsInstance(peers, list)
        for item in peers:
            self.assertIsInstance(item.id, str)
            self.assertIsInstance(item.name, str)
            self.assertIsInstance(item.network, str)
            self.assertIsInstance(item.owner_id, str)
            self.assertIsInstance(item.owner_name, str)
            self.assertIsInstance(item.color, str)
            self.assertIsInstance(item.extensions, dict)
            self.assertIsInstance(item.software_versions, node.SoftwerVersionModel)
            self.assertIsInstance(item.address, str)
            self.assertIsInstance(item.port, int)
    
    def test_api_version(self):
        version = self.api.api_version
        self.assertIsInstance(version, str)
    
    def test_apps(self):
        apps = self.api.list_apps()
        self.assertIsInstance(apps, apps_models.AppsModel)
    
    def test_interlockings(self):
        interlocks = self.api.list_interlockings(
            self.default_chain
        )
        self.assertEqual(interlocks.page, 0)
        self.assertEqual(interlocks.page_size, 10)
        self.assertFalse(interlocks.last_to_first)
        self.assertIsInstance(interlocks.items, list)
        for item in interlocks.items:
            self.assertIsInstance(item, records.InterlockingRecordModel)
        if len(interlocks.items) > 1:
            self.assertGreaterEqual(interlocks.items[1].created_at, interlocks.items[0].created_at)
    
    def test_interlockings_params(self):
        interlocks = self.api.list_interlockings(
            self.default_chain,
            page=1,
            size=2,
            last_to_first=True,
        )
        self.assertEqual(interlocks.page, 1)
        self.assertEqual(interlocks.page_size, 2)
        self.assertTrue(interlocks.last_to_first)
        self.assertIsInstance(interlocks.items, list)
        for item in interlocks.items:
            self.assertIsInstance(item, records.InterlockingRecordModel)
    
    def test_list_mirrors(self):
        mirrors = self.api.list_mirrors()
        self.assertIsInstance(mirrors, list)
        for item in mirrors:
            self.assertIsInstance(item, chains.ChainIdModel)