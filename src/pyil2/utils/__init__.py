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
from typing import List, Self
from cryptography.hazmat.primitives import ciphers


def aes_decrypt(msg: bytes, key: bytes, iv: bytes) -> bytes:
    """
    AES decryptor.

    Args:
        msg (:obj:`bytes`): Encrypted message.
        key (:obj:`bytes`): AES key.
        iv (:obj:`bytes`): AES IV.

    Returns:
        :obj:`bytes`: Decrypted message.
    """
    cipher = ciphers.Cipher(ciphers.algorithms.AES(key), ciphers.modes.CBC(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(msg) + decryptor.finalize()


class AppPermissions:
    def __init__(self, app_id: int, action_ids: List[int] = list):
        """
        Apps permissions model.

        Args:
            app_id (:obj:`int`): App identifier.
            actions_ids ([:obj:`int`]): List of actions.
        """
        self.app_id = app_id
        self.action_ids = action_ids

    @classmethod
    def resolve(cls, permissions: str) -> Self:
        """
        Parse a string into an :obj:`AppPermissions` object.

        Args:
            permissions (:obj:`str`): App permissions in the format used by \
                the JSON response ('#<appId>,<actionId_1>,...,<actionId_n>').

        Returns:
            :obj:`AppPermissions`: return an :obj:`AppPermissions` instance.
        """
        permissions = permissions.replace('#', '').strip()
        p = permissions.split(',')
        app_id = int(p[0])
        action_ids = [int(item) for item in p[1:]]
        return cls(app_id=app_id, action_ids=action_ids)

    def __str__(self):
        """ 
        :obj:`str`: String representation of app permissions 
            in the JSON format ('#<appId>[,<actionId_1>,...,<actionId_n>]').
        """
        if self.action_ids:
            return f"#{self.app_id},{','.join([str(item) for item in self.action_ids])}"
        return f"#{self.app_id}"
