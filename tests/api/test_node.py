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
from src.pyil2.models import chain
from .base import BaseApiTest
from src.pyil2.models import (
    node,
    apps as apps_models,
    record,
)


class NodeApiTest(BaseApiTest):
    def setUp(self):
        super().setUp()
        self.api = self.client.api('node')

    def test_details(self):
        details = self.api.details
        self.assertIsInstance(details.id, str)
        self.assertIsInstance(details.name, str)
        self.assertIsInstance(details.network, str)
        self.assertIsInstance(details.owner_id, str)
        self.assertIsInstance(details.owner_name, str)
        self.assertIsInstance(details.peer_address, str)
        self.assertIsInstance(details.color, str)
        self.assertIsInstance(details.chains, list)
        self.assertIsInstance(details.extensions, dict)
        self.assertIsInstance(details.software_versions,
                              node.SoftwareVersionModel)

    def test_peers(self):
        peers = self.api.list_peers()
        self.assertIsInstance(peers, list)
        for item in peers:
            self.assertIsInstance(item.id, str)
            self.assertIsInstance(item.name, str)
            self.assertIsInstance(item.network, str)
            self.assertIsInstance(item.owner_id, str)
            self.assertIsInstance(item.owner_name, str)
            self.assertIsInstance(item.color, str)
            self.assertIsInstance(item.extensions, dict)
            self.assertIsInstance(item.software_versions,
                                  node.SoftwareVersionModel)
            self.assertIsInstance(item.address, str)
            self.assertIsInstance(item.port, int)

    def test_api_version(self):
        version = self.api.api_version
        self.assertIsInstance(version, str)

    def test_apps(self):
        apps = self.api.list_apps()
        self.assertIsInstance(apps, apps_models.AppsModel)

    def test_interlockings_to(self):
        interlocks = self.api.list_interlockings_to_chain(
            self.default_chain
        )
        self.assertEqual(interlocks.page, 0)
        self.assertEqual(interlocks.page_size, 10)
        self.assertFalse(interlocks.last_to_first)
        self.assertIsInstance(interlocks.items, list)
        for item in interlocks.items:
            self.assertIsInstance(item, record.InterlockingRecordModel)
        if len(interlocks.items) > 1:
            self.assertGreaterEqual(
                interlocks.items[1].created_at, interlocks.items[0].created_at)

    def test_interlockings_params(self):
        interlocks = self.api.list_interlockings_to_chain(
            self.default_chain,
            page=1,
            size=2,
            last_to_first=True,
        )
        # self.assertEqual(interlocks.page, 1)
        self.assertEqual(interlocks.page_size, 2)
        self.assertTrue(interlocks.last_to_first)
        self.assertIsInstance(interlocks.items, list)
        for item in interlocks.items:
            self.assertIsInstance(item, record.InterlockingRecordModel)

    def test_list_mirrors(self):
        mirrors = self.api.list_mirrors()
        self.assertIsInstance(mirrors, list)
        for item in mirrors:
            self.assertIsInstance(item, chain.ChainIdModel)

    def test_add_mirrors(self):
        resp = self.api.add_mirrors(
            ['xsNzHsq6Xiew1wukwJsCSDDhNvwHgb5Q-Njv_QB-Kng'])
        self.assertTrue(resp)
