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
from typing import Self


class LimitedRange:
    """ 
    A closed interval of integers represented by the notation '[start-end]'.
    If the range has only one value, the range is represented by '[start]'.

    Args:
            start (:obj:`int`): Initial value of the interval.
            count (:obj:`int`): How many elements are in the range. 
            end (:obj:`int`): If defined, define the end value of the interval.

    Raises:
        ValueError: If 'count' is 0

    Attributes:
        start (:obj:`int`): Initial value of the interval
        end (:obj:`int`): End value of the interval

    """

    def __init__(self, start: int, count: int = 1, end: int = None) -> None:
        if count == 0:
            raise ValueError('Count is out of range')

        self.start = start
        if end is None:
            self.end = start + count - 1
        else:
            self.end = end

    @property
    def count(self) -> int:
        """:obj:`int`: Number of elements in the interval."""
        return self.end - self.start + 1

    @classmethod
    def resolve(cls, text: str) -> Self:
        """ 
        Parses a string into a :obj:`LimitedRange`.

        Args:
            text (:obj:`str`): String representing the range in the \
                format of '[start]' or '[start-end]'.

        Returns:
            :obj:`LimitedRange`: An instance of the LimitedRange represented by the `text`."""
        parts = text.replace('[', '').replace(']', '').split('-')
        if len(parts) == 1:
            return cls(int(parts[0]))
        return cls(int(parts[0]), end=int(parts[1]))

    def __str__(self) -> str:
        """ :obj:`str`: String representation of self. """
        return f"[{self.start}{f'-{self.end}' if self.start != self.end else ''}]"

    def __eq__(self, other: Self) -> bool:
        """ :obj:`bool`: Return self == other."""
        return self.start == other.start and self.end == other.end

    def __contains__(self, item: int | Self) -> bool:
        """ 
        Check if item is in self.

        Args:
            item (:obj:`int`/:obj:`LimitedRange`): Item to check if is in self.

        Returns:
            :obj:`bool`: Return item in self.
        """
        if isinstance(item, LimitedRange):
            return self.__contains__(item.start) and self.__contains__(item.end)
        return self.start <= item <= self.end

    def overlaps_with(self, other: Self) -> bool:
        """
        Check if there is an overlap between the intervals of self and other.

        Returns:
            :obj:`bool`: Return True if there is an overlap.
        """
        return other.start in self or other.end in self or self in other
