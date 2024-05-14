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
    List,
    Dict,
    Any,
    Optional,
)

import base64
from json import loads as json_loads
from pydantic import Field
from pyilint import ilint_decode

from ..enum import CipherAlgorithms
from .base import BaseCamelModel
from .record import BaseRecordModel
from ..utils.certificates import PKCS12Certificate
from ..utils import aes_decrypt


class ReaderKeyModel(BaseCamelModel):
    """
    Reader key model.
    """

    name: str
    """
    Name of the reader key
    """
    public_key: str
    """
    IL2 text representation of a public key to encrypt the content for.
    """


class AllowedReadersModel(BaseCamelModel):
    """
    List of allow readers model.
    """

    contextId: str
    """
    Allowed readers list name.
    """
    readers: List[ReaderKeyModel] = Field(default_factory=list)
    """
    List of reader keys.
    """


class AllowedReadersDetailsModel(AllowedReadersModel):
    """
    Allowed readers details model.
    """

    record_reference: Optional[str] = None
    """
    A record reference in the form chainId@recordSerial
    """


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
        if not certificate.has_pk():
            raise ValueError(
                'Certificate has no private key to be able to decode EncryptedText.')
        cert_key_id = certificate.key_id
        cert_pub_key_hash = certificate.pub_key_hash
        if not cert_pub_key_hash:
            raise ValueError('Non-RSA certificate is not currently supported.')

        if cert_key_id != self.reader_id or cert_pub_key_hash != self.public_key_hash:
            return False
        return True


class EncryptedTextModel(BaseCamelModel):
    """
    JSON Documents encrypted text.
    """

    cipher: CipherAlgorithms
    """
    Cipher algorithm used to cipher the text.
    """
    cipher_text: Optional[str] = ''
    """
    Encrypted text.
    """
    reading_keys: List[ReadingKeyModel]
    """
    List of keys able to read this encrypted text.
    """

    def decode(self, certificate: PKCS12Certificate) -> Dict[str, Any]:
        """
        Decodes the encrypted JSON text to a dictionary using a given certificate.

        Args:
            certificate (:obj:`utils.certificate.PKCS12Certificate`): PKCS12 certificate.

        Returns:
            {:obj:`str`: Any}: Decoded JSON.

        Raises:
            `ValueError`: If there is no encrypted text or the certificate is not \
                in the reading keys.

        """
        if not self.cipher:
            raise ValueError(' No cipher detected.')
        if self.cipher != CipherAlgorithms.AES256.value:
            raise ValueError(
                f'Cipher {self.cipher} is not currently supported.')

        authorized_key = None
        for rk in self.reading_keys:
            if rk.check_certificate(certificate):
                authorized_key = rk
                break
        if not authorized_key:
            raise ValueError(
                'Your key does not match one of the authorized reading keys.')

        aes_key = certificate.decrypt(
            base64.urlsafe_b64decode(authorized_key.encrypted_key))
        aes_iv = certificate.decrypt(
            base64.urlsafe_b64decode(authorized_key.encrypted_iv))

        json_bytes = aes_decrypt(base64.urlsafe_b64decode(
            self.cipher_text), aes_key, aes_iv)
        if json_bytes[0] != 17:
            raise ValueError(
                'Something went wrong while decrypting the content. Unexpected initial bytes.')

        dec, dec_size = ilint_decode(json_bytes[1:])
        return json_loads(json_bytes[1+dec_size:1+dec_size+dec].decode('utf-8'))


class JsonDocumentModel(BaseRecordModel):
    """
    Record to store JSON documents.
    """

    encrypted_json: Optional[EncryptedTextModel] = None
    """
    JSON Documents encrypted text.
    """
    json_text: Optional[str] = None
    """
    JSON document as string.
    """
