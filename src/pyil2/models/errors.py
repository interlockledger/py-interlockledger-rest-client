from typing import Optional
from .base import BaseCamelModel

class ErrorDetailsModel(BaseCamelModel):
    """
    Error details model.
    """

    type: Optional[str] = None
    """
    Error type.
    """
    title: Optional[str] = None
    """
    Error title.
    """
    status: Optional[int] = None
    """
    Error status code.
    """
    detail: Optional[str] = None
    """
    Error details.
    """
    instance: Optional[str] = None
    """
    Error instance.
    """
    