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
    def __init__(self, path: str, password: str) :
        self._friendly_name = ''
        self._pkcs12_cert = self._get_cert_from_file(path, password)
    
    @property
    def common_name(self) -> str:
        """:obj:`str`: Certificate Common Name. If none found, return empty string."""
        cn = self._pkcs12_cert[1].subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        if not cn :
            return ''
        return cn[0].value

    @property
    def friendly_name(self) -> str:
        """:obj:`str`: Certificate friendly name (Not implemented)."""
        #return self._pkcs12_cert.get_friendlyname()
        return self._friendly_name

    @property
    def private_key(self) -> bytes:
        """:obj:`bytes`: Certificate private key."""
        #return crypto.dump_privatekey(crypto.FILETYPE_PEM, self._pkcs12_cert.get_privatekey())
        return self._pkcs12_cert[0].private_bytes(encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption())
    
    @property
    def public_certificate(self) -> bytes:
        """:obj:`bytes`: Certificate public certificate."""
        #return crypto.dump_certificate(crypto.FILETYPE_PEM, self._pkcs12_cert.get_certificate())
        return self._pkcs12_cert[1].public_bytes(encoding=serialization.Encoding.PEM)

    @property
    def key_id(self) -> str:
        """:obj:`str`: Id of the key."""
        digest = hashes.Hash(hashes.SHA1())
        digest.update(self._pkcs12_cert[1].public_bytes(encoding=serialization.Encoding.DER))
        s = base64.urlsafe_b64encode(digest.finalize()).decode().replace('=','')
        return f'Key!{s}#SHA1'

    @property
    def pub_key_hash(self) -> str:
        """:obj:`str`: Public key hash in IL2 text representation."""
        if not self._pkcs12_cert[1] :
            return None
        modulus = self._pkcs12_cert[1].public_key().public_numbers().n
        exponet = self._pkcs12_cert[1].public_key().public_numbers().e
        
        writer = io.BytesIO()
        t = pyiltags.ILRawTag(16, modulus.to_bytes((modulus.bit_length()+7)//8, byteorder='big'))
        t.serialize(writer)
        modulus_tag = writer.getvalue()

        writer = io.BytesIO()
        t = pyiltags.ILRawTag(16, exponet.to_bytes((exponet.bit_length()+7)//8, byteorder='big'))
        t.serialize(writer)
        exponet_tag = writer.getvalue()

        writer = io.BytesIO()
        t = pyiltags.ILRawTag(40, modulus_tag+exponet_tag)
        t.serialize(writer)
        pub_key_parameter_tag = writer.getvalue()

        digest = hashes.Hash(hashes.SHA256())
        digest.update(pub_key_parameter_tag)
        s = base64.urlsafe_b64encode(digest.finalize()).decode().replace('=','')
        
        return f'{s}#SHA256'
        

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
        with open(os.path.expanduser(cert_path), 'rb') as f :
            pkcs_cert = pkcs12.load_key_and_certificates(f.read(), cert_pass.encode())
        return pkcs_cert
