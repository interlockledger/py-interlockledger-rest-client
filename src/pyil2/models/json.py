from typing import (
    List,
    Optional
)

from pydantic import Field
from ..enum import CipherAlgorithms
from .base import BaseCamelModel
from .record import BaseRecordModel
from ..utils.certificates import PKCS12Certificate
import datetime

class ReadingKeyModel(BaseCamelModel):
    """
    Keys able to read an encrypted JSON Document record.
    """

    encrypted_iv: Optional[str] = Field(alias='encryptedIV', default=None)
    """
    Encrypted AES256 IV.
    """
    encrypted_key: Optional[str] = None
    """
    Encrypted AES256 key.
    """
    public_key_hash: Optional[str] = None
    """
    Public key hash in IL2 text representation.
    """
    reader_id: Optional[str] = None
    """
    Id of the key.
    """
    

    def check_certificate(self, certificate: PKCS12Certificate) -> bool:
        """
        Checks if a PKCS12 certificate corresponds to this reading key.

        Args:
            certificate (:obj:`utils.certificate.PKCS12Certificate`): PKCS12 certificate.
        
        Returns:
            `bool`: Returns `True` if the certificate corresponds to this reading key.
        
        Raises:
            `ValueError`: If the certificate has no private key or are a Non-RSA certificate. 
        """
        if not certificate.has_pk() :
            raise ValueError('Certificate has no private key to be able to decode EncryptedText.')
        cert_key_id = certificate.key_id
        cert_pub_key_hash = certificate.pub_key_hash
        if not cert_pub_key_hash :
            raise ValueError('Non-RSA certificate is not currently supported.')

        if cert_key_id != self.reader_id or cert_pub_key_hash != self.public_key_hash:
            return False
        return True

class EncryptedTextModel(BaseCamelModel):
    cipher: CipherAlgorithms
    cipher_text: Optional[str] = None
    reading_keys: List[ReadingKeyModel]

class JsonDocumentModel(BaseRecordModel):
    encrypted_json: None
    json_text: Optional[str]