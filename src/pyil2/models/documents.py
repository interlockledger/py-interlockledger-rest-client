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
from typing import (
    Optional,
    List,
)
import datetime
from pydantic import (
    Field,
    model_validator,
)
from .base import BaseCamelModel
from ..enum import DocumentsCompression


class DocumentUploadConfigurationModel(BaseCamelModel):
    """
    Node configuration of uploaded documents.
    """

    default_compression: Optional[str] = None
    """
    Default compression algorithm.
    """
    default_encryption: Optional[str] = None
    """
    Default encryption algorithm.
    """
    file_size_limit: Optional[int] = None
    """
    Maximum file size.
    """
    iterations: Optional[int] = None
    """
    Default number of PBE iterations to generate the key.
    """
    permitted_content_types: List[str] = Field(default_factory=list)
    """
    List of content types mime-type concatenated with acceptable filename extensions.
    """
    timeout_in_minutes: int = Field(alias='timeOutInMinutes', default=0)
    """
    Timeout in minutes.
    """


class BaseDocumentTransactionModel(BaseCamelModel):
    """
    Base document transaction model.
    """

    chain_id: str = Field(alias='chain')
    """
    Id of the chain where the set of documents should be stored.
    """
    comment: Optional[str] = None
    """
    Any additional information about the set of documents to be stored.
    """
    compression: Optional[DocumentsCompression] = None
    """
    Compression algorithm.
    """
    encryption: Optional[str] = None
    """
    The encryption descriptor in the <pbe>-<hash>-<cipher>-<level> format. Examples: \n
        - "PBKDF2-SHA256-AES256-LOW" 
        - "PBKDF2-SHA512-AES256-MID"
        - "PBKDF2-SHA256-AES128-HIGH"
    """
    generate_public_directory: bool = True
    """
    If the publically viewable PublicDirectory field should be created.
    """
    previous: Optional[str] = None
    """
    Reference to a previous document locator.
    """


class BeginDocumentTransactionModel(BaseDocumentTransactionModel):
    """
    Begin document transaction model.
    """

    iterations: Optional[int] = None
    """
    Override for the number of PBE iterations to generate the key.
    """
    password: Optional[str] = Field(default=None, min_length=12)
    """
    Password as bytes if `encryption` is not null.
    """
    previous_documents_not_to_copy: List[int] = Field(default_factory=list)
    """
    List of documents in the previous record to be excluded in this record.
    If nothing is passed, copy every document from the previous document to this record.
    """
    allow_children: bool = True
    """
    If `True`, allows this document record to be updated by children records.
    """
    to_children_comment: Optional[str] = None
    """
    Comment added for children records.
    """

    @model_validator(mode='after')
    def validate_encrypted_password(self):
        """
        Validate if password is missing when encryption is defined.
        """
        if self.encryption and not self.password:
            raise ValueError('Password is required if encryption is defined.')
        return self


class DocumentTransactionModel(BaseDocumentTransactionModel):
    """
    Document transaction status model.
    """

    can_commit_now: bool = False
    """
    If `True`, the transaction is able to be committed.
    """
    count_of_uploaded_documents: int = 0
    """
    Total count of uploaded documents for this transaction.
    """
    document_names: List[str] = Field(default_factory=list)
    """
    List of documents uploaded in the transaction.
    """
    timeout_limit: datetime.datetime = Field(alias='timeOutLimit')
    """
    The transaction will be aborted if not completed until this timeout.
    """
    transaction_id: str
    """
    ID of the transaction to use when uploading each file and committing the transaction.
    """


class EncryptionParameterModel(BaseCamelModel):
    """
    The parameters used to make the encryption of the set of documents.
    """

    iterations: int = 0
    """
    Number of iterations to generate the key.
    """
    salt: Optional[str] = None
    """
    Salt value to feed the cypher engine.
    """


class DirectoryEntryModel(BaseCamelModel):
    """
    Entry details for each stored document in this documents record.
    """

    comment: Optional[str] = None
    """
    Additional comment for the document entry.
    """
    mime_type: Optional[str] = None
    """
    Mime Type for the document content.
    """
    name: Optional[str] = None
    """
    Document file name.
    """
    path: Optional[str] = None
    """
    Relative path of the file in the public directory
    """
    hash_sha256: Optional[str] = Field(alias='hashSHA256', default=None)
    """
    SHA256 hash of the file bytes.
    """
    size: Optional[int] = 0
    """
    File size in bytes.
    """


class DocumentMetadataModel(BaseCamelModel):
    """
    Documents metadata model.
    """
    record_reference: Optional[str] = None
    """
    Universal reference of this record.
    """
    creation_time: datetime.datetime
    """
    Time of record creation.
    """
    comment: Optional[str] = None
    """
    Any additional information about this set of documents.
    """
    compression: Optional[str] = None
    """
    Compression algorithm.
    """
    encryption: Optional[str] = None
    """
    The encryption descriptor in the <pbe>-<hash>-<cipher>-<level> format.
    """
    encryption_parameters: Optional[EncryptionParameterModel] = None
    """
    The parameters used to make the encryption of the set of documents.
    """
    public_directory: List[DirectoryEntryModel] = Field(default_factory=list)
    """
    List of stored documents.
    """
