from unittest import TestCase
from src.pyil2.models import chain
import datetime

class ChainIdModelTest(TestCase):
    def test_up(self):
        data = {
            "id": "chain_id",
            "lastRecord": 40,
            "lastUpdate": "2023-10-17T21:00:02.015+00:00",
            "licensingStatus": "Perpetually licensed",
            "name": "Chain name",
            "sizeInBytes": 74153,
            "isClosedForNewTransactions": False,
        }
        model = chain.ChainIdModel(**data)
        self.assertFalse(model.closed)
        data["isClosedForNewTransactions"] = True
        model = chain.ChainIdModel(**data)
        self.assertTrue(model.closed)
        