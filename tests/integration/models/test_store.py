import unittest

from models.item import ItemModel
from tests.integration.integration_base_test import BaseTest
from models.store import StoreModel

class MyTestCase(BaseTest):

    def test_create_store_items_empty(self):
        store_item = StoreModel("Store_1")

        self.assertListEqual(store_item.items.all(), [])

    def test_crud_SQLlite(self):
        with self.app_context():

            store_item = StoreModel("Store_1")

            self.assertIsNone(StoreModel.find_by_name("Store_1"))

            store_item.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name("Store_1"))

            store_item.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name("Store_1"))

    def test_store_relationship(self):
        with self.app_context():
            store_item = StoreModel("Store_1")
            item_model = ItemModel("Beer", 5.19, 1)

            store_item.save_to_db()
            item_model.save_to_db()

            self.assertEqual(store_item.items.count(), 1)
            self.assertEqual(store_item.items.first().name, "Beer")

    def test_empty_items_json(self):
        store_item = StoreModel("Store_1")
        expected = {
            "id": None,
            "name": "Store_1",
            "items": [],
        }

        self.assertEqual(store_item.json(), expected)

    def test_items_json(self):
        with self.app_context():
            store_item = StoreModel("Store_1")
            item_model = ItemModel("Beer", 5.19, 1)

            store_item.save_to_db()
            item_model.save_to_db()
            expected = {
                "id": 1,
                "name": "Store_1",
                "items": [{
                        "name": "Beer",
                        "price": 5.19
                     }],
            }

            self.assertEqual(store_item.json(), expected)


if __name__ == '__main__':
    unittest.main()
