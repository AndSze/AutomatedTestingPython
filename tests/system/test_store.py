import json

from models.store import StoreModel
from models.item import ItemModel
from tests.system.system_base_test import BaseTest

class Store(BaseTest):

    def test_create_store(self):
        with self.app() as client:
            with self.app_context():

                response = client.post("/store/Test_store")

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name("Test_store"))
                self.assertDictEqual({'id': 1,'name': "Test_store", "items": []},
                                     json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():

                client.post("/store/Test_store")
                response = client.post("/store/Test_store")

                self.assertEqual(response.status_code, 400)
                self.assertIsNotNone(StoreModel.find_by_name("Test_store"))
                self.assertDictEqual({'message': "A store with name 'Test_store' already exists."},
                                     json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():

                client.post("/store/Test_store")

                self.assertIsNotNone(StoreModel.find_by_name("Test_store"))

                response = client.delete("/store/Test_store")
                self.assertEqual(response.status_code, 200)
                self.assertIsNone(StoreModel.find_by_name("Test_store"))
                self.assertDictEqual({'message': "Store deleted"},
                                     json.loads(response.data))

    def test_delete_non_existent_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/Test_store")

                self.assertIsNotNone(StoreModel.find_by_name("Test_store"))

                response = client.delete("/store/Test_store")
                self.assertEqual(response.status_code, 200)
                self.assertIsNone(StoreModel.find_by_name("Test_store"))
                self.assertDictEqual({'message': "Store deleted"},
                                     json.loads(response.data))

                response = client.delete("/store/Test_store")
                self.assertEqual(response.status_code, 200)
                self.assertIsNone(StoreModel.find_by_name("Test_store"))
                self.assertDictEqual({'message': "Store to be deleted does not exist"},
                                     json.loads(response.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/Test_store")

                self.assertIsNotNone(StoreModel.find_by_name("Test_store"))

                response = client.get("/store/Test_store")
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'id': 1, 'name': "Test_store", "items": []},
                                     json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():

                response = client.get("/store/Test_store")
                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({'message': "Store not found"},
                                     json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():

                client.post("/store/Test_store")
                client.post("/item/Test_item", data={"price": 5.19, "store_id": 1})

                response = client.get("/store/Test_store")
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'id': 1, 'name': "Test_store", "items": [{
                                                                                'name': 'Test_item',
                                                                                'price': 5.19
                                                                               }],
                                      'name': 'Test_store'},
                                     json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/Test_store")

                response = client.get("/stores")
                self.assertDictEqual({'stores': [{
                                                    'id': 1,
                                                    'name': "Test_store",
                                                    "items": []
                                                }]
                                     },
                                     json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():

                client.post("/store/Test_store")
                client.post("/item/Test_item", data={"price": 5.19, "store_id": 1})

                response = client.get("/stores")
                self.assertDictEqual({'stores': [{
                                                    'id': 1,
                                                    'name': "Test_store",
                                                    "items": [{
                                                                'name': 'Test_item',
                                                                'price': 5.19
                                                              }],
                                                }]
                                     },
                                     json.loads(response.data))