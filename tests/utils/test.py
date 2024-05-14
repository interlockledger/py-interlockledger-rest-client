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
from unittest import TestCase
from src.pyil2.utils import AppPermissions


class AppPermissionsTest(TestCase):
    def test_resolve(self):
        data = '#0,131'
        permissions = AppPermissions.resolve(data)
        self.assertEqual(permissions.app_id, 0)
        self.assertListEqual(permissions.action_ids, [131])
        self.assertEqual(str(permissions), data)

        data = '#2,500,501'
        permissions = AppPermissions.resolve(data)
        self.assertEqual(permissions.app_id, 2)
        self.assertListEqual(permissions.action_ids, [500, 501])
        self.assertEqual(str(permissions), data)

        data = '#4'
        permissions = AppPermissions.resolve(data)
        self.assertEqual(permissions.app_id, 4)
        self.assertListEqual(permissions.action_ids, [])
        self.assertEqual(str(permissions), data)

    def test_constructor(self):
        data = '#0,131'
        permissions = AppPermissions(app_id=0, action_ids=[131])
        self.assertEqual(permissions.app_id, 0)
        self.assertListEqual(permissions.action_ids, [131])
        self.assertEqual(str(permissions), data)

        data = '#2,500,501'
        permissions = AppPermissions(app_id=2, action_ids=[500, 501])
        permissions = AppPermissions.resolve(data)
        self.assertEqual(permissions.app_id, 2)
        self.assertListEqual(permissions.action_ids, [500, 501])
        self.assertEqual(str(permissions), data)

        data = '#4'
        permissions = AppPermissions(app_id=4)
        permissions = AppPermissions.resolve(data)
        self.assertEqual(permissions.app_id, 4)
        self.assertListEqual(permissions.action_ids, [])
        self.assertEqual(str(permissions), data)
