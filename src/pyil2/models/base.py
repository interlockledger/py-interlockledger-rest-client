from typing import Dict, Generic, List, Self, TypeVar
from pydantic import (
    BaseModel,
    ConfigDict,
    TypeAdapter,
)
from pydantic.alias_generators import to_camel

T = TypeVar('T')

class BaseCamelModel(BaseModel):
    """
    Base model able to serializes/deserialize JSON data with camelCase field names.
    """
    
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        validate_default=True,
    )

    @classmethod
    def validate_list_python(cls, entries: List[Dict[str, any]]) -> List[Self]:
        """
        Validates a list of standard python objects and returns a list of objects
        of this class. It will raise a ValidationError from pydantic if the input
        is not valid.
        """
        if not isinstance(entries, list):
            raise ValueError('entries must be a list of basic.')
        if not hasattr(cls, '__array_type_adapter'):
            cls.__array_type_adapter = TypeAdapter(List[cls])
        return cls.__array_type_adapter.validate_python(entries)

class ListModel(BaseCamelModel, Generic[T]):
    """
    Base paginated list model.
    """

    page: int = 0
    """
    Current page number.
    """
    total_number_of_pages: int = 0
    """
    Total number of pages.
    """
    page_size: int = 0
    """
    Number of items in the page.
    """
    last_to_first: bool = False
    """
    If `True`, the list of items will be in from newer to older.
    """
    items: List[T]
    """
    List of items.
    """
