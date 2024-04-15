from typing import (
    Optional,
    List,
)
import datetime
from pydantic import Field
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
    password: Optional[str] = None
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
    

class DocumentTransactionModel(BaseDocumentTransactionModel):
    """
    Document transaction status model.
    """
    
    can_commit_now: bool
    """
    If `True`, the transaction is able to be committed.
    """
    count_of_uploaded_documents: int
    """
    Total count of uploaded documents for this transaction.
    """
    document_names: List[str]
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
    

