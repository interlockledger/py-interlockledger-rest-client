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
from pydantic import ValidationError
from .base import BaseApiTest
import requests
import os
from src.pyil2.models.errors import ErrorDetailsModel
from src.pyil2.models import documents as documents_models


class DocumentsApiTest(BaseApiTest):
    def setUp(self):
        super().setUp()
        self.api = self.client.api('documents')

    def test_documents_configuration(self):
        config = self.api.documents_configuration
        self.assertIsInstance(
            config, documents_models.DocumentUploadConfigurationModel)

    def test_document_upload(self):
        new_transaction = documents_models.BeginDocumentTransactionModel(
            chain=self.default_chain
        )
        transaction = self.api.begin_document_transaction(new_transaction)
        self.assertIsInstance(
            transaction, documents_models.DocumentTransactionModel)

        status = self.api.get_document_transaction_status(
            transaction.transaction_id)
        self.assertIsInstance(
            transaction, documents_models.DocumentTransactionModel)
        self.assertEqual(transaction.transaction_id, status.transaction_id)

        transaction = self.api.upload_document(
            transaction_id=transaction.transaction_id,
            filename='test.txt',
            content_type='text/plain',
            file_bytes=b'file 1',
        )
        self.assertIsInstance(
            transaction, documents_models.DocumentTransactionModel)
        self.assertGreaterEqual(len(transaction.document_names), 1)

        locator = self.api.commit_document_transaction(
            transaction.transaction_id)
        self.assertIsInstance(locator, str)
        self.assertFalse('$' in locator)

        metadata = self.api.get_document_metadata(locator)
        self.assertIsInstance(metadata, documents_models.DocumentMetadataModel)

        document_path = self.api.download_single_document_at(locator, 1)
        self.assertIsInstance(document_path, str)
        self.assertTrue(os.path.isfile(document_path))
        os.remove(document_path)

        document_zip = self.api.download_documents_as_zip(locator)
        self.assertIsInstance(document_zip, str)
        self.assertTrue(os.path.isfile(document_zip))
        os.remove(document_zip)

        document_response = self.api.download_single_document_at_as_response(
            locator, 1)
        self.assertIsInstance(document_response, requests.Response)

        document_zip_response = self.api.download_documents_as_zip_as_response(
            locator)
        self.assertIsInstance(document_zip_response, requests.Response)

    def test_document_upload_file(self):
        filepath = './filename.txt'
        with open(filepath, 'wb') as f:
            f.write(b'Test filepath.')

        new_transaction = documents_models.BeginDocumentTransactionModel(
            chain=self.default_chain
        )
        transaction = self.api.begin_document_transaction(new_transaction)
        self.assertIsInstance(
            transaction, documents_models.DocumentTransactionModel)

        status = self.api.get_document_transaction_status(
            transaction.transaction_id)
        self.assertIsInstance(
            transaction, documents_models.DocumentTransactionModel)
        self.assertEqual(transaction.transaction_id, status.transaction_id)

        transaction = self.api.upload_document_file(
            transaction_id=transaction.transaction_id,
            filepath=filepath,
        )
        self.assertIsInstance(
            transaction, documents_models.DocumentTransactionModel)
        self.assertGreaterEqual(len(transaction.document_names), 1)

        locator = self.api.commit_document_transaction(
            transaction.transaction_id)
        self.assertIsInstance(locator, str)
        self.assertFalse('$' in locator)

        metadata = self.api.get_document_metadata(locator)
        self.assertIsInstance(metadata, documents_models.DocumentMetadataModel)

    def test_document_upload_file_force_name_content(self):
        filepath = './filename.txt'
        with open(filepath, 'wb') as f:
            f.write(b'{"attr": "value"}')

        new_transaction = documents_models.BeginDocumentTransactionModel(
            chain=self.default_chain
        )
        transaction = self.api.begin_document_transaction(new_transaction)
        self.assertIsInstance(
            transaction, documents_models.DocumentTransactionModel)

        status = self.api.get_document_transaction_status(
            transaction.transaction_id)
        self.assertIsInstance(
            transaction, documents_models.DocumentTransactionModel)
        self.assertEqual(transaction.transaction_id, status.transaction_id)

        transaction = self.api.upload_document_file(
            transaction_id=transaction.transaction_id,
            filepath=filepath,
            filename='data.json',
            content_type='application/json'
        )
        self.assertIsInstance(
            transaction, documents_models.DocumentTransactionModel)
        self.assertGreaterEqual(len(transaction.document_names), 1)

        locator = self.api.commit_document_transaction(
            transaction.transaction_id)
        self.assertIsInstance(locator, str)
        self.assertFalse('$' in locator)

        metadata = self.api.get_document_metadata(locator)
        self.assertIsInstance(metadata, documents_models.DocumentMetadataModel)

        found = False
        for item in metadata.public_directory:
            if item.name == 'data.json':
                found = True
                self.assertEqual(item.mime_type, 'application/json')
        self.assertTrue(found)

        os.remove(filepath)

    def test_document_upload_encrypted_comment(self):
        doc_comment = 'This is a comment'
        file_comment = 'File comment'
        new_transaction = documents_models.BeginDocumentTransactionModel(
            chain=self.default_chain,
            comment=doc_comment,
            encryption='PBKDF2-SHA512-AES256-MID',
            password='1234567890123456'
        )
        transaction = self.api.begin_document_transaction(new_transaction)

        transaction = self.api.upload_document(
            transaction_id=transaction.transaction_id,
            filename='test.txt',
            content_type='text/plain',
            file_bytes=b'file 1',
            comment=file_comment
        )
        locator = self.api.commit_document_transaction(
            transaction.transaction_id)
        self.assertIsInstance(locator, str)
        self.assertTrue('$' in locator)

        metadata = self.api.get_document_metadata(locator)
        self.assertIsInstance(metadata, documents_models.DocumentMetadataModel)
        self.assertEqual(metadata.comment, doc_comment)
        for item in metadata.public_directory:
            if item.name == 'test.txt':
                self.assertEqual(item.comment, file_comment)

        locator_without_password = locator.split('$')[0]

        document_response = self.api.download_single_document_at_as_response(
            locator_without_password, 1)
        self.assertIsInstance(document_response, ErrorDetailsModel)

        document_response = self.api.download_single_document_at_as_response(
            locator, 1)
        self.assertIsInstance(document_response, requests.Response)

    def test_documents_update(self):
        new_transaction = documents_models.BeginDocumentTransactionModel(
            chain=self.default_chain,
            comment='This is a comment',
            encryption='PBKDF2-SHA512-AES256-MID',
            password='1234567890123456'
        )
        transaction = self.api.begin_document_transaction(new_transaction)

        transaction = self.api.upload_document(
            transaction_id=transaction.transaction_id,
            filename='file1.txt',
            content_type='text/plain',
            file_bytes=b'file 1',
            comment='File comment'
        )
        locator = self.api.commit_document_transaction(
            transaction.transaction_id)

        metadata = self.api.get_document_metadata(locator)

        new_transaction = documents_models.BeginDocumentTransactionModel(
            chain=self.default_chain,
            comment='This is a comment',
            encryption='PBKDF2-SHA512-AES256-MID',
            password='1234567890123456',
            previous=locator,
        )
        update_transaction = self.api.begin_document_transaction(
            new_transaction)

        update_transaction = self.api.upload_document(
            transaction_id=update_transaction.transaction_id,
            filename='file2.txt',
            content_type='text/plain',
            file_bytes=b'file 2',
            comment='File comment'
        )
        new_locator = self.api.commit_document_transaction(
            update_transaction.transaction_id)
        new_metadata = self.api.get_document_metadata(new_locator)
        self.assertGreater(len(new_metadata.public_directory),
                           len(metadata.public_directory))
        index = 0
        for idx, item in enumerate(new_metadata.public_directory):
            if item.name == 'file1.txt':
                index = idx

        new_transaction = documents_models.BeginDocumentTransactionModel(
            chain=self.default_chain,
            comment='This is a comment',
            encryption='PBKDF2-SHA512-AES256-MID',
            password='1234567890123456',
            previous=new_locator,
            previous_documents_not_to_copy=[index]
        )
        remove_transaction = self.api.begin_document_transaction(
            new_transaction)
        remove_locator = self.api.commit_document_transaction(
            remove_transaction.transaction_id)
        remove_metadata = self.api.get_document_metadata(remove_locator)

        found = False
        for item in remove_metadata.public_directory:
            if item.name == 'file1.txt':
                found = True
        self.assertFalse(found)

    def test_documents_update_not_valid(self):
        new_transaction = documents_models.BeginDocumentTransactionModel(
            chain=self.default_chain,
            comment='This is a comment',
            encryption='PBKDF2-SHA512-AES256-MID',
            password='1234567890123456',
            allow_children=False,
        )
        transaction = self.api.begin_document_transaction(new_transaction)

        transaction = self.api.upload_document(
            transaction_id=transaction.transaction_id,
            filename='file1.txt',
            content_type='text/plain',
            file_bytes=b'file 1',
            comment='File comment'
        )
        locator = self.api.commit_document_transaction(
            transaction.transaction_id)

        new_transaction = documents_models.BeginDocumentTransactionModel(
            chain=self.default_chain,
            comment='This is a comment',
            encryption='PBKDF2-SHA512-AES256-MID',
            password='1234567890123456',
            previous=locator,
        )
        update_transaction = self.api.begin_document_transaction(
            new_transaction)
        self.assertIsInstance(update_transaction, ErrorDetailsModel)

    def test_document_upload_encrypted_short_password(self):
        with self.assertRaises(ValidationError):
            new_transaction = documents_models.BeginDocumentTransactionModel(
                chain=self.default_chain,
                encryption='PBKDF2-SHA512-AES256-MID',
                password='12345678901'
            )

    def test_document_upload_encrypted_no_password(self):
        with self.assertRaises(ValueError):
            new_transaction = documents_models.BeginDocumentTransactionModel(
                chain=self.default_chain,
                encryption='PBKDF2-SHA512-AES256-MID'
            )

    def test_document_metadata_not_found(self):
        locator = self.default_chain + 'A'

        resp = self.api.get_document_metadata(locator)
        self.assertIsInstance(resp, ErrorDetailsModel)

    def test_download_single_not_found(self):
        locator = self.default_chain + 'A'

        resp = self.api.download_single_document_at(locator, 10)
        self.assertIsInstance(resp, ErrorDetailsModel)

    def test_download_zip_not_found(self):
        locator = self.default_chain + 'A'

        resp = self.api.download_documents_as_zip(locator)
        self.assertIsInstance(resp, ErrorDetailsModel)

    def test_download_single_response_not_found(self):
        locator = self.default_chain + 'A'

        resp = self.api.download_single_document_at_as_response(locator, 10)
        self.assertIsInstance(resp, ErrorDetailsModel)

    def test_download_zip_response_not_found(self):
        locator = self.default_chain + 'A'

        resp = self.api.download_documents_as_zip_as_response(locator)
        self.assertIsInstance(resp, ErrorDetailsModel)
