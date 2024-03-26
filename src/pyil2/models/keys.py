from typing import List, Optional

from pydantic import field_serializer, field_validator

from ..utils.certificates import PKCS12Certificate

from ..utils import AppPermissions
from .base import BaseCamelModel
from ..enum import KeyPurpose

class CertificatePermitModel(BaseCamelModel):
    name: str
    """
    Key name. Must match the name imported in te node.
    """
    permissions: List[AppPermissions]
    """
    List of Apps and Corresponding Actions to be permitted by numbers.
    """
    purposes: List[KeyPurpose]
    """
    Key valid purposes.
    """
    certificate_in_X509: str
    """
    The public certificate in PEM encoding in base64.
    """

    @field_validator('certificate_in_X509', mode='before')
    @classmethod
    def pre_process_certificate(cls, raw: PKCS12Certificate) -> str:
        """
        Deserialize permissions field
        """
        if isinstance(raw, str):
            return raw
        return (raw
                .public_certificate.decode('utf-8')
                .replace('-----BEGIN CERTIFICATE-----','')
                .replace('-----END CERTIFICATE-----','')
                .replace('\n',''))

    
    @field_validator('permissions', mode='before')
    @classmethod
    def pre_process_permissions(cls, raw: List[str]) -> List[AppPermissions]:
        """
        Deserialize permissions field
        """
        ret = []
        for item in raw:
            if isinstance(item, str):
                item = AppPermissions.resolve(item)
            ret.append(item)
        return ret

    @field_serializer('permissions')
    @classmethod
    def serialize_reserved_tags(cls, value: List[AppPermissions]) -> List[str]:
        """
        Serialize permissions field.
        """
        ret = []
        for item in value:
            ret.append(str(item))
        return ret


class ExportedKeyFileModel(BaseCamelModel):
    """
    Key file info.
    """

    key_file_bytes: Optional[bytes] = None
    """
    Key file in bytes.
    """
    key_file_name: Optional[str] = None
    """
    Filename of the key.
    """
    key_name: Optional[str] = None
    """
    Name of the key.
    """
    