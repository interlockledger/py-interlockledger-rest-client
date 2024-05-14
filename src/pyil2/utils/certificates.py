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
import io
import os
import base64
from cryptography.x509 import NameOID, Certificate
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import pyiltags


class PKCS12Certificate:
    """ 
    A PKCS12 certificate interface.    

    Args:
            path (:obj:`str`): Path to the .pfx certificate. 
            password (:obj:`str`): Password of the .pfx certificate.
    """

    def __init__(self, path: str, password: str):
        self._friendly_name = ''
        self._pkcs12_cert = self._get_cert_from_file(path, password)

    @property
    def common_name(self) -> str:
        """:obj:`str`: Certificate Common Name. If none found, return empty string."""
        cn = self._pkcs12_cert[1].subject.get_attributes_for_oid(
            NameOID.COMMON_NAME)
        if not cn:
            return ''
        return cn[0].value

    @property
    def friendly_name(self) -> str:
        """:obj:`str`: Certificate friendly name (Not implemented)."""
        # return self._pkcs12_cert.get_friendlyname()
        return self._friendly_name

    @property
    def private_key(self) -> bytes:
        """:obj:`bytes`: Certificate private key."""
        # return crypto.dump_privatekey(crypto.FILETYPE_PEM, self._pkcs12_cert.get_privatekey())
        return self._pkcs12_cert[0].private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

    @property
    def public_certificate(self) -> bytes:
        """:obj:`bytes`: Certificate public certificate."""
        # return crypto.dump_certificate(crypto.FILETYPE_PEM, self._pkcs12_cert.get_certificate())
        return self._pkcs12_cert[1].public_bytes(encoding=serialization.Encoding.PEM)

    @property
    def key_id(self) -> str:
        """:obj:`str`: Id of the key."""
        digest = hashes.Hash(hashes.SHA1())
        digest.update(self._pkcs12_cert[1].public_bytes(
            encoding=serialization.Encoding.DER))
        s = base64.urlsafe_b64encode(
            digest.finalize()).decode().replace('=', '')
        return f'Key!{s}#SHA1'

    @property
    def pub_key_hash(self) -> str:
        """:obj:`str`: Public key hash in IL2 text representation."""
        pub_key_parameter_tag = self._format_pub_key()
        if pub_key_parameter_tag is None:
            return None

        digest = hashes.Hash(hashes.SHA256())
        digest.update(pub_key_parameter_tag)
        s = base64.urlsafe_b64encode(
            digest.finalize()).decode().replace('=', '')

        return f'{s}#SHA256'

    @property
    def pub_key(self) -> str:
        """:obj:`str`: Public key in IL2 text representation."""
        pub_key_parameter_tag = self._format_pub_key()
        if pub_key_parameter_tag is None:
            return None

        s = base64.urlsafe_b64encode(
            pub_key_parameter_tag).decode().replace('=', '')

        return f'PubKey!{s}#RSA'

    @property
    def public_modulus(self) -> int:
        """:obj:`int`: Public modulus."""
        return self._pkcs12_cert[1].public_key().public_numbers().n

    @property
    def public_exponent(self) -> int:
        """:obj:`int`: Public exponent."""
        return self._pkcs12_cert[1].public_key().public_numbers().e

    def has_pk(self) -> bool:
        """
        Check if the certificate has a primary key.

        Returns:
            :obj:`bool`: True if the certificate has a primary key.
        """
        return self._pkcs12_cert[0] is not None

    def decrypt(self, cypher_text: bytes) -> bytes:
        """
        Decode a encrypted message using RSA with SHA1.

        Args:
            cypher_text (:obj:`bytes`): Encrypted message.

        Returns:
            :obj:`bytes`: Decrypted message.
        """
        msg = self._pkcs12_cert[0].decrypt(cypher_text, padding=padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        ))
        return msg

    def _get_cert_from_file(self, cert_path: str, cert_pass: str) -> Certificate:
        with open(os.path.expanduser(cert_path), 'rb') as f:
            pkcs_cert = pkcs12.load_key_and_certificates(
                f.read(), cert_pass.encode())
        return pkcs_cert

    def _format_pub_key(self) -> bytes | None:
        if not self._pkcs12_cert[1]:
            return None
        modulus = self._pkcs12_cert[1].public_key().public_numbers().n
        exponet = self._pkcs12_cert[1].public_key().public_numbers().e

        writer = io.BytesIO()
        t = pyiltags.ILRawTag(16, modulus.to_bytes(
            (modulus.bit_length()+7)//8, byteorder='big'))
        t.serialize(writer)
        modulus_tag = writer.getvalue()

        writer = io.BytesIO()
        t = pyiltags.ILRawTag(16, exponet.to_bytes(
            (exponet.bit_length()+7)//8, byteorder='big'))
        t.serialize(writer)
        exponet_tag = writer.getvalue()

        writer = io.BytesIO()
        t = pyiltags.ILRawTag(40, modulus_tag+exponet_tag)
        t.serialize(writer)
        pub_key_parameter_tag = writer.getvalue()
        return pub_key_parameter_tag
