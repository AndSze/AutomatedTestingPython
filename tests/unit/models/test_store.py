from models.store import StoreModel
from tests.unit.unit_base_test import BaseTest
import unittest


class StoreTest(BaseTest):

    def setUp(self):
        self.store_model = StoreModel("Store_1")

    def test_ItemModel_class_properties(self):
        self.assertIsNotNone(StoreModel.id)
        self.assertIsNotNone(StoreModel.name)
        self.assertIsNotNone(StoreModel.items)

    def test_StoreModel_constructor(self):
        self.assertEqual(self.store_model.name, "Store_1",
                         "The name of the store after creation does not equal the constructor argument.")

if __name__ == '__main__':
    unittest.main()
