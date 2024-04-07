from .base import BaseApiTest
from src.pyil2.models.errors import ErrorDetailsModel
from src.pyil2.models.record import OpaqueRecordModel

class OpaqueApiTest(BaseApiTest):
    def setUp(self):
        super().setUp()
        self.api = self.client.api('opaque')
    
    def test_opaque(self):
        opaque = self.api.add_opaque(
            chain_id=self.default_chain,
            application_id=13,
            payload_type_id=1313,
            payload=b'test'
        )
        self.assertIsInstance(opaque, OpaqueRecordModel)
    

    def test_opaque_last_changed_serial_error(self):
        opaque = self.api.add_opaque(
            chain_id=self.default_chain,
            application_id=13,
            payload_type_id=1313,
            payload=b'test',
            last_changed_serial=0
        )
        self.assertIsInstance(opaque, ErrorDetailsModel)
    