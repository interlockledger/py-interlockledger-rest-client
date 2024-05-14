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
from typing import List, Optional

from pydantic import field_serializer, field_validator

from ..utils.certificates import PKCS12Certificate

from ..utils import AppPermissions
from .base import BaseCamelModel
from ..enum import KeyPurpose


class BaseKeyModel(BaseCamelModel):
    """
    Base key model.
    """

    name: Optional[str] = None
    """
    Key name. Must match the name imported in the node.
    """
    permissions: List[AppPermissions]
    """
    List of Apps and Corresponding Actions to be permitted by numbers.
    """
    purposes: List[KeyPurpose]
    """
    Key valid purposes.
    """

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


class KeyDetailsModel(BaseKeyModel):
    """
    Key details model
    """

    id: str
    """
    Unique key id.
    """
    public_key: str
    """
    Key public key.
    """


class CertificatePermitModel(BaseKeyModel):
    """
    Certificate permit model.
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
                .replace('-----BEGIN CERTIFICATE-----', '')
                .replace('-----END CERTIFICATE-----', '')
                .replace('\n', ''))


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
