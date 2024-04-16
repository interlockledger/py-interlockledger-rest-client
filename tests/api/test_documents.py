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

    def test_document_upload(self):
        new_transaction = documents_models.BeginDocumentTransactionModel(
            chain=self.default_chain
        )
        transaction = self.api.begin_document_transaction(new_transaction)
        self.assertIsInstance(transaction, documents_models.DocumentTransactionModel)

        status = self.api.get_document_transaction_status(transaction.transaction_id)
        self.assertIsInstance(transaction, documents_models.DocumentTransactionModel)
        self.assertEqual(transaction.transaction_id, status.transaction_id)

        transaction = self.api.upload_document(
            transaction_id=transaction.transaction_id,
            filename='test.txt',
            content_type='text/plain',
            file_bytes=b'file 1',
        )
        self.assertIsInstance(transaction, documents_models.DocumentTransactionModel)
        self.assertGreaterEqual(len(transaction.document_names), 1)
