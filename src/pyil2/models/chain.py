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
import datetime
from typing import List, Optional

from pydantic import Field

from .keys import (
    CertificatePermitModel,
    ExportedKeyFileModel,
)

from ..enum import (
    KeyStrength,
    Algorithms,
)

from .base import BaseCamelModel


class ChainIdModel(BaseCamelModel):
    """
    Chain summary.
    """

    id: str
    """
    Chain ID.
    """
    closed: bool = Field(alias='isClosedForNewTransactions', default=False)
    """
    If `True`, this chain is not able to accept new records.
    """
    last_record: int = 0
    """
    Last record (serial number).
    """
    last_update: datetime.datetime
    """
    Date last record was added.
    """
    licensing_status: Optional[str] = None
    """
    Licensing status.
    """
    name: Optional[str] = None
    """
    Chain name.
    """
    size_in_bytes: int = 0
    """
    Chain size in bytes.
    """


class ChainCreatedModel(ChainIdModel):
    """
    Chain created response.
    """

    key_files: List[ExportedKeyFileModel] = Field(default_factory=list)
    """
    Key file names.
    """


class ChainSummaryModel(ChainIdModel):
    """
    Chain summary.
    """

    active_apps: List[int] = Field(default_factory=list)
    """
    List of active apps (only the numeric ids).
    """
    description: Optional[str] = None
    """
    Chain description.
    """
    is_mirror: bool = False
    """
    If `True`, this chain is a mirror copy from an outside node.
    """


class ChainCreationModel(BaseCamelModel):
    """
    Chain creation model.
    """
    addional_apps: List[int] = Field(default_factory=list)
    """
    List of additional apps (only numeric ids).
    """
    api_certificates: Optional[List[CertificatePermitModel]] = None
    """
    List of certificates to permit in the chain.
    """
    description: Optional[str] = None
    """
    Description (perhaps intended primary usage).
    """
    emergency_closing_key_password: str = Field(min_length=1)
    """
    Emergency closing key password.
    """
    emergency_closing_key_strength: KeyStrength = Field(
        default=KeyStrength.EXTRA_STRONG)
    """
    Emergency closing key strength of key.
    """
    keys_algorithm: Optional[Algorithms] = Field(default=None)
    """
    Keys algorithm.
    """
    management_key_password: str = Field(min_length=1)
    """
    Key management key password.
    """
    management_key_strength: KeyStrength = Field(default=KeyStrength.STRONG)
    """
    Key management strength of key.
    """
    name: str = Field(min_length=1)
    """
    Name of the chain.
    """
    operating_key_strength: KeyStrength = Field(default=KeyStrength.NORMAL)
    """
    Operating key strength of key.
    """
    operating_key_algorithm: Optional[Algorithms] = Field(default=None)
    """
    Operating key algorithm.
    """
    parent: Optional[str] = None
    """
    Parent chain ID.
    """
