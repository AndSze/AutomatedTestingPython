import unittest

from models.store import StoreModel
from tests.integration.integration_base_test import BaseTest
from models.item import ItemModel

class ItemTest(BaseTest):

    def test_crud_SQLlite(self):
        with self.app_context():

            item_model = ItemModel("Beer", 5.19, 1)

            self.assertIsNone(ItemModel.find_by_name("Beer")) # make sure it does not exit in db before saving it to db

            item_model.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name("Beer"))

            item_model.delete_from_db()

            # works because in SQLite, store_id is a foreign key, but store object has not been created
            self.assertIsNone(ItemModel.find_by_name("Beer"))

    def test_crud_Postgres(self):
        with self.app_context():
            store_item = StoreModel("Store_1")
            item_model = ItemModel("Beer", 5.19, 1)

            self.assertIsNone(ItemModel.find_by_name("Beer"))  # make sure it does not exit in db before saving it to db
            self.assertIsNone(StoreModel.find_by_name("Store_1"))

            store_item.save_to_db()
            item_model.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name("Beer"))
            self.assertIsNotNone(StoreModel.find_by_name("Store_1"))

            store_item.delete_from_db()
            item_model.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name("Beer"))
            self.assertIsNone(StoreModel.find_by_name("Store_1"))

    def test_store_relationship(self):
        with self.app_context():
            store_item = StoreModel("Store_1")
            item_model = ItemModel("Beer", 5.19, 1)

            item_model.save_to_db()
            store_item.save_to_db()

            self.assertEqual(item_model.store.name, "Store_1")


if __name__ == '__main__':
    unittest.main()