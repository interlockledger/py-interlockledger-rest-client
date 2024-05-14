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
from enum import Enum
from enum import IntEnum
from enum import auto

class Algorithms(Enum):
    """
    Enumeration of the digital signature algorithms available in IL2.
    """
    RSA = 'RSA'        # PKCS#1 RSASSA-PSS
    """
    PKCS#1 RSASSA-PSS
    """
    RSA15 = 'RSA15'      # RSASSA-PKCS1-v1_5
    """
    RSASSA-PKCS1-v1_5
    """
    DSA = 'DSA'
    """
    DSA
    """
    ElGamal = 'ElGamal'
    """
    ElGamal signature
    """
    EcDSA = 'EcDSA'
    """
    Elliptic Curve Digital Signature Algorithm
    """
    EdDSA = 'EdDSA'
    """
    Edwards-curve Digital Signature Algorithm
    """


class DataFieldCast(Enum):
    """
    Enumeration of casting options for DataField
    """
    NONE = 'None'
    """
    """
    DateTime = 'DateTime'
    """
    """
    Integer = 'Integer'
    """
    """
    TimeSpan = 'TimeSpan'
    """
    """


class CipherAlgorithms(Enum):
    """
    Enumeration of the cipher algorithms available in IL2.
    """
    NONE = 'None'
    """
    """
    AES256 = 'AES256'  # default
    """
    """

    @classmethod
    def _missing_(cls, value):
        return CipherAlgorithms.AES256


class HashAlgorithms(Enum):
    """
    Enumeration of the hash algorithms available in IL2.
    """
    SHA256 = 'SHA256'   # default
    """
    """
    SHA1 = 'SHA1'
    """
    """
    SHA512 = 'SHA512'
    """
    """
    SHA3_256 = 'SHA3_256'
    """
    """
    SHA3_512 = 'SHA3_512'
    """
    """
    Copy = 'Copy'
    """
    """


class KeyPurpose(Enum):
    """
    Enumeration of the purpose of keys in IL2.
    """
    Action = 'Action'
    """
    """
    ChainOperation = 'ChainOperation'
    """
    """
    Encryption = 'Encryption'
    """
    """
    ForceInterlock = 'ForceInterlock'
    """
    """
    KeyManagement = 'KeyManagement'
    """
    """
    Protocol = 'Protocol'
    """
    """
    InvalidKey = 'InvalidKey'
    """
    """
    ClaimSigner = 'ClaimSigner'
    """
    """


class KeyStrength(Enum):
    """
    Enumeration of the strength of keys.
    """
    # Attributes:
    #    Normal : RSA 2048
    #    Strong : RSA 3072
    #    ExtraStrong : RSA 4096
    #    MegaStrong : RSA 5120
    #    SuperStrong : RSA 6144
    #    HyperStrong : RSA 7172
    #    UltraStrong : RSA 8192

    Normal = 'Normal'        # RSA 2048
    """
    RSA 2048
    """
    Strong = 'Strong'        # RSA 3072
    """
    RSA 3072
    """
    ExtraStrong = 'ExtraStrong'   # RSA 4096
    """
    RSA 4096
    """
    MegaStrong = 'MegaStrong'    # RSA 5120
    """
    RSA 5120
    """
    SuperStrong = 'SuperStrong'   # RSA 6144
    """
    RSA 6144
    """
    HyperStrong = 'HyperStrong'   # RSA 7172
    """
    RSA 7172
    """
    UltraStrong = 'UltraStrong'   # RSA 8192
    """
    RSA 8192
    """


class NetworkProtocol(Enum):
    """
    Enumeration of the network protocols.
    """
    TCP_Direct = 'TCP_Direct'
    """
    """
    TCP_Proxied = 'TCP_Proxied'
    """
    """
    HTTPS_Proxied = 'HTTPS_Proxied'
    """
    """
    Originator_Only = 'Originator_Only'
    """
    """


class NetworkPredefinedPorts(IntEnum):
    """
    Enumeration of the default ports of the IL2 networks.
    """
    MainNet = 32032
    """
    """
    MetaNet = 32036
    """
    """
    TestNet_Jupiter = 32030
    """
    """
    TestNet_Saturn = 32028
    """
    """
    TestNet_Neptune = 32026
    """
    """
    TestNet_Minerva = 32024
    """
    """
    TestNet_Janus = 32022
    """
    """
    TestNet_Apollo = 32020
    """
    """
    TestNet_Liber = 32018
    """
    """


class RecordType(Enum):
    """
    Enumeration of the types of Records available in IL2.
    """
    Data = 'Data'
    """
    """
    Root = 'Root'
    """
    """
    Closing = 'Closing'
    """
    """
    EmergencyClosing = 'EmergencyClosing'
    """
    """
    Corrupted = 'Corrupted'
    """
    """


class DocumentsCompression(Enum):
    """
    Enumeration of the compression algorithm.
    """
    NONE = 'NONE'
    """
    """
    GZIP = 'GZIP'
    """
    """
    BROTLI = 'BROTLI'
    """
    """
    ZSTD = 'ZSTD'
    """
    """
