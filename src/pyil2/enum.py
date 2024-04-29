from enum import Enum
from enum import IntEnum
from enum import auto

class AutoName(Enum) :
    """
    Base Enum class to automatically generate the enumerations values based on the enumeration name.
    """
    def _generate_next_value_(name, start, count, last_values):
        return name

class Algorithms(AutoName) :
    """
    Enumeration of the digital signature algorithms available in IL2.
    """
    RSA = auto()        # PKCS#1 RSASSA-PSS
    """
    PKCS#1 RSASSA-PSS
    """
    RSA15 = auto()      # RSASSA-PKCS1-v1_5
    """
    RSASSA-PKCS1-v1_5
    """
    DSA = auto()        
    """
    DSA
    """
    ElGamal = auto()   
    """
    ElGamal signature
    """
    EcDSA = auto()
    """
    Elliptic Curve Digital Signature Algorithm
    """
    EdDSA = auto()
    """
    Edwards-curve Digital Signature Algorithm
    """
    


class DataFieldCast(AutoName) :
    """
    Enumeration of casting options for DataField
    """
    NONE = 'None'
    """
    """
    DateTime = auto()
    """
    """
    Integer = auto()
    """
    """
    TimeSpan = auto()
    """
    """
    

class CipherAlgorithms(AutoName) :
    """
    Enumeration of the cipher algorithms available in IL2.
    """
    NONE = 'None'   
    """
    """
    AES256 = auto() # default
    """
    """
    
    @classmethod
    def _missing_(cls, value):
        return CipherAlgorithms.AES256   

class HashAlgorithms(AutoName) :
    """
    Enumeration of the hash algorithms available in IL2.
    """
    SHA256 = auto()   # default
    """
    """
    SHA1 = auto()
    """
    """
    SHA512 = auto()
    """
    """
    SHA3_256 = auto()
    """
    """
    SHA3_512 = auto()
    """
    """
    Copy = auto()
    """
    """
    

class KeyPurpose(AutoName) :
    """
    Enumeration of the purpose of keys in IL2.
    """
    Action = auto()
    """
    """
    ChainOperation = auto()
    """
    """
    Encryption = auto()
    """
    """
    ForceInterlock = auto()
    """
    """
    KeyManagement = auto()
    """
    """
    Protocol = auto()
    """
    """
    InvalidKey = auto()
    """
    """
    ClaimSigner = auto()
    """
    """
    

class KeyStrength(AutoName) :
    """
    Enumeration of the strength of keys.
    """
    #Attributes:
    #    Normal : RSA 2048
    #    Strong : RSA 3072
    #    ExtraStrong : RSA 4096
    #    MegaStrong : RSA 5120
    #    SuperStrong : RSA 6144
    #    HyperStrong : RSA 7172
    #    UltraStrong : RSA 8192
    
    Normal = auto()        # RSA 2048
    """
    RSA 2048
    """
    Strong = auto()        # RSA 3072
    """
    RSA 3072
    """
    ExtraStrong = auto()   # RSA 4096
    """
    RSA 4096
    """
    MegaStrong = auto()    # RSA 5120
    """
    RSA 5120
    """
    SuperStrong = auto()   # RSA 6144
    """
    RSA 6144
    """
    HyperStrong = auto()   # RSA 7172
    """
    RSA 7172
    """
    UltraStrong = auto()   # RSA 8192
    """
    RSA 8192
    """


class NetworkProtocol(AutoName) :
    """
    Enumeration of the network protocols.
    """
    TCP_Direct = auto()
    """
    """
    TCP_Proxied = auto()
    """
    """
    HTTPS_Proxied = auto()
    """
    """
    Originator_Only = auto()
    """
    """
    

class NetworkPredefinedPorts(IntEnum) :
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
    


class RecordType(AutoName) :
    """
    Enumeration of the types of Records available in IL2.
    """
    Data = auto()
    """
    """
    Root = auto()
    """
    """
    Closing = auto()
    """
    """
    EmergencyClosing = auto()
    """
    """
    Corrupted = auto()
    """
    """
    
class DocumentsCompression(AutoName) :
    """
    Enumeration of the compression algorithm.
    """
    NONE = auto()
    """
    """
    GZIP = auto()
    """
    """
    BROTLI = auto()
    """
    """
    ZSTD = auto()
    """
    """
    