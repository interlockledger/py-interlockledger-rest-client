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
        #self.assertEqual(interlocks.page_size, 10)
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
        #self.assertEqual(interlocks.page, 1)
        #self.assertEqual(interlocks.total_number_of_pages, 3)
        #self.assertEqual(interlocks.page_size, 2)
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
        keys_to_permit= []
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