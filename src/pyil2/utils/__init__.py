

from typing import List, Self


class AppPermissions:
    def __init__(self, app_id: int, action_ids: List[int]=list):
        self.app_id = app_id
        self.action_ids = action_ids
    
    @classmethod
    def resolve(cls, permissions: str) -> Self:
        """
        Parse a string into an :obj:`AppPermissions` object.

        Args:
            permissions (:obj:`str`): App permissions in the format used by the JSON response ('#<appId>,<actionId_1>,...,<actionId_n>').

        Returns:
            :obj:`AppPermissions`: return an :obj:`AppPermissions` instance.
        """
        permissions = permissions.replace('#','').strip()
        p = permissions.split(',')
        app_id = int(p[0])
        action_ids = [int(item) for item in p[1:]]
        return cls(app_id=app_id, action_ids=action_ids)

    def __str__(self):
        """ :obj:`str`: String representation of app permissions in the JSON format ('#<appId>[,<actionId_1>,...,<actionId_n>]')."""
        if self.action_ids :
            return f"#{self.app_id},{','.join([str(item) for item in self.action_ids])}"
        return f"#{self.app_id}"