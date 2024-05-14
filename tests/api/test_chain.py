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
from .base import BaseApiTest
from src.pyil2.models import (
    chain as chain_models,
    errors,
    keys as keys_models,
    record,
)


class ChainApiTest(BaseApiTest):
    def setUp(self):
        super().setUp()
        self.api = self.client.api('chain')

    def test_list_chains(self):
        chains = self.api.list_chains()
        self.assertIsInstance(chains, list)
        for item in chains:
            self.assertIsInstance(item, chain_models.ChainIdModel)

    def test_create_chain(self):
        new_chain = chain_models.ChainCreationModel(
            name="Chain name",
            emergency_closing_key_password="emergencyPassword",
            management_key_password="managementPassword",
        )

        created = self.api.create_chain(new_chain)
        self.assertIsInstance(created, chain_models.ChainCreatedModel)
        self.assertIsInstance(created.id, str)

    def test_chain_summary(self):
        chain = self.api.summary(self.default_chain)
        self.assertIsInstance(chain, chain_models.ChainSummaryModel)

    def test_list_active_apps(self):
        apps = self.api.list_active_apps(self.default_chain)
        self.assertIsInstance(apps, list)
        for item in apps:
            self.assertIsInstance(item, int)

    def test_add_active_apps_invalid_app(self):
        apps = self.api.add_active_apps(self.default_chain, [10000])
        self.assertIsInstance(apps, errors.ErrorDetailsModel)

    def test_list_interlockings(self):
        interlocks = self.api.list_interlockings(self.default_chain)
        self.assertEqual(interlocks.page, 0)
        # self.assertEqual(interlocks.page_size, 10)
        self.assertIsInstance(interlocks.items, list)
        for item in interlocks.items:
            self.assertIsInstance(item, record.InterlockingRecordModel)

    def test_list_interlockings_params(self):
        interlocks = self.api.list_interlockings(
            self.default_chain,
            page=1,
            size=2,
            how_many_from_last=5,
        )
        # self.assertEqual(interlocks.page, 1)
        # self.assertEqual(interlocks.total_number_of_pages, 3)
        # self.assertEqual(interlocks.page_size, 2)
        self.assertIsInstance(interlocks.items, list)
        for item in interlocks.items:
            self.assertIsInstance(item, record.InterlockingRecordModel)

    def test_force_interlock(self):
        interlock = record.ForceInterlockModel(target_chain=self.second_chain)
        response = self.api.force_interlocking(self.default_chain, interlock)
        self.assertIsInstance(response, record.InterlockingRecordModel)

    def test_list_keys(self):
        keys = self.api.list_keys(self.default_chain)
        self.assertIsInstance(keys, list)
        for item in keys:
            self.assertIsInstance(item, keys_models.KeyDetailsModel)

    def test_add_keys(self):
        keys = self.api.list_keys(self.default_chain)
        keys_to_permit = []
        for item in keys:
            if item.name.find("rest.api") < 0:
                continue
            keys_to_permit.append(item)
        keys = self.api.add_keys(
            self.default_chain,
            keys_to_permit=keys_to_permit
        )
        self.assertIsInstance(keys, list)
        for item in keys:
            self.assertIsInstance(item, keys_models.KeyDetailsModel)

    def test_add_keys_empty(self):
        keys = self.api.add_keys(
            self.default_chain,
            keys_to_permit=[]
        )
        self.assertIsInstance(keys, errors.ErrorDetailsModel)
