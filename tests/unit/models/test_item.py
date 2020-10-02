import unittest
from models.item import ItemModel
from tests.unit.unit_base_test import BaseTest

class ItemTest(BaseTest):

    def setUp(self):
        self.item_model = ItemModel("Beer", 5.19, 1)

    def test_ItemModel_constructor(self):
        self.assertEqual(self.item_model.name, "Beer",
                         "The name of the item after creation does not equal the constructor argument.")
        self.assertEqual(self.item_model.price, 5.19,
                         "The price of the item after creation does not equal the constructor argument.")

        self.assertEqual(self.item_model.store_id, 1)

    def test_json(self):
        expected = {
            "name": "Beer",
            "price": 5.19,
        }
        self.assertEqual(self.item_model.json(), expected,
                         "The JSON export of the item is incorrect. Received {}, expected {}."
                         .format(self.item_model.json(), expected))

    def test_ItemModel_class_properties(self):
        self.assertIsNotNone(ItemModel.name)
        self.assertIsNotNone(ItemModel.price)
        self.assertIsNotNone(ItemModel.id)
        self.assertIsNotNone(ItemModel.store_id)
        self.assertIsNotNone(ItemModel.store)

    # the below methods interact with db - cannot test on unit test level unless the db is mocked
    # find_by_name(cls, name), def save_to_db(self), def delete_from_db(self):

if __name__ == '__main__':
    unittest.main()
