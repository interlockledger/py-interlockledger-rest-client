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