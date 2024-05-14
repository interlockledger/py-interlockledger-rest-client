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
