from .base import BaseApiTest
import os
from src.pyil2.models.errors import ErrorDetailsModel
from src.pyil2.models import documents as documents_models

class DocumentsApiTest(BaseApiTest):
    def setUp(self):
        super().setUp()
        self.api = self.client.api('documents')
        
    def test_documents_configuration(self):
        config = self.api.documents_configuration
        self.assertIsInstance(config, documents_models.DocumentUploadConfigurationModel)