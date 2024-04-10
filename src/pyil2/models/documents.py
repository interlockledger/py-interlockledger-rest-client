from typing import (
    Optional,
    List,
)
from pydantic import Field
from .base import BaseCamelModel


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
    
