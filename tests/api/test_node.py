from .base import BaseApiTest
from src.pyil2.models import node

class NodeApiTest(BaseApiTest):
    def setUp(self):
        super().setUp()
        self.api = self.client.api('node')
    
    def test_details(self):
        details = self.api.details()
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
        peers = self.api.peers()
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