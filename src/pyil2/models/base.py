from typing import Dict, List, Self
from pydantic import (
    BaseModel,
    ConfigDict,
    TypeAdapter,
)
from pydantic.alias_generators import to_camel

class BaseCamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
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

class ListModel(BaseCamelModel):
    """
    Base paginated list model.
    """

    page: int=0
    """
    Current page number.
    """
    total_number_of_pages: int
    """
    Total number of pages.
    """
    page_size: int
    """
    Number of items in the page.
    """
    last_to_first: bool
    """
    If `True`, the list of items will be in from newer to older.
    """
    items: List[BaseCamelModel]
    """
    List of items.
    """
