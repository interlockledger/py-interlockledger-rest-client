

from typing import Self


class LimitedRange :
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
    def __init__(self, start: int, count: int=1, end: int=None) -> None:
        if count == 0 :
            raise ValueError(f'count is out of range')
        
        self.start = start  
        if end is None :
            self.end = start + count - 1
        else :
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
            text (:obj:`str`): String representing the range in the format of '[start]' or '[start-end]'.
        
        Returns:
            :obj:`LimitedRange`: An instance of the LimitedRange represented by the `text`."""
        parts = text.replace('[','').replace(']','').split('-')
        if len(parts) == 1:
            return cls(int(parts[0]))
        else :
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
        if type(item) is LimitedRange :
            return self.__contains__(item.start) and self.__contains__(item.end)
        else :
            return (self.start <= item) and (item <= self.end)

    def overlaps_with(self, other: Self) -> bool:
        """
        Check if there is an overlap between the intervals of self and other.

        Returns:
            :obj:`bool`: Return True if there is an overlap.
        """
        return other.start in self or other.end in self or self in other
