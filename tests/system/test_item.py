import json

from models.store import StoreModel
from models.item import ItemModel
from tests.system.system_base_test import BaseTest

class ItemTest(BaseTest):

    def setUp(self):
        # Pythonic way of calling a method from parent class, otherwise it is overwritten by child's class method implementation
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():

                client.post("/register", data={"username": "test", "password": "1234"})
                auth_response = client.post('/auth',
                                           data=json.dumps({"username": "test", "password": "1234"}),
                                           headers={"Content-Type": "application/json"})

                self.assertIn("access_token", json.loads(auth_response.data).keys())  # ["access_token", ....]
                auth_token = json.loads(auth_response.data)['access_token']
                self.access_token = f"JWT {auth_token}"

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():

                client.post("/store/Test_store")
                response = client.post("/item/Test_item", data={"price": 5.19, "store_id": 1})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(ItemModel.find_by_name("Test_item"))
                self.assertDictEqual({'name': 'Test_item', 'price': 5.19},
                                     json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/Test_store")
                client.post("/item/Test_item", data={"price": 5.19, "store_id": 1})
                response = client.post("/item/Test_item", data={"price": 5.19, "store_id": 1})

                self.assertEqual(response.status_code, 400)
                self.assertIsNotNone(ItemModel.find_by_name("Test_item"))
                self.assertDictEqual({'message': "An item with name 'Test_item' already exists."},
                                     json.loads(response.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():

                client.post("/store/Test_store")
                client.post("/item/Test_item", data={"price": 5.19, "store_id": 1})

                self.assertIsNotNone(ItemModel.find_by_name("Test_item"))

                response = client.delete("/item/Test_item")
                self.assertEqual(response.status_code, 200)
                self.assertIsNone(ItemModel.find_by_name("Test_item"))
                self.assertDictEqual({'message': "Item deleted"},
                                     json.loads(response.data))

    def test_delete_non_existent_item(self):
        with self.app() as client:
            with self.app_context():

                client.post("/store/Test_store")

                response = client.delete("/item/Test_item")
                self.assertEqual(response.status_code, 200)
                self.assertIsNone(ItemModel.find_by_name("Test_item"))
                self.assertDictEqual({'message': "Item to be deleted does not exist"},
                                     json.loads(response.data))

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():

                client.post("/store/Test_store")
                client.post("/item/Test_item", data={"price": 5.19, "store_id": 1})
                response = client.get("/item/Test_item", headers={"Authorization": self.access_token})

                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(ItemModel.find_by_name("Test_item"))
                self.assertDictEqual({'name': 'Test_item', 'price': 5.19},
                                     json.loads(response.data))

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():

                response = client.get("/item/Test_item", headers={"Authorization": self.access_token})

                self.assertEqual(response.status_code, 404)
                self.assertIsNone(ItemModel.find_by_name("Test_item"))
                self.assertDictEqual({'message': 'Item not found'},
                                     json.loads(response.data))

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():

                client.post("/store/Test_store")
                client.post("/item/Test_item", data={"price": 5.19, "store_id": 1})
                response = client.get("/item/Test_item")

                self.assertEqual(response.status_code, 401) # due to @jwt_required
                self.assertDictEqual({"message": "Could not authorize. Did you include a valid Authorization header?"},
                                     json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():

                client.post("/store/Test_store")
                response = client.put("/item/Test_item", data={"price": 5.19, "store_id": 1})

                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(ItemModel.find_by_name("Test_item"))
                self.assertDictEqual({'name': 'Test_item', 'price': 5.19},
                                     json.loads(response.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():

                client.post("/store/Test_store_1")
                response = client.put("/item/Test_item", data={"price": 5.19, "store_id": 1})

                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(ItemModel.find_by_name("Test_item"))
                self.assertDictEqual({'name': 'Test_item', 'price': 5.19},
                                     json.loads(response.data))

                response = client.put("/item/Test_item", data={"price": 5.99, "store_id": 1})

                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(ItemModel.find_by_name("Test_item"))
                self.assertDictEqual({'name': 'Test_item', 'price': 5.99},
                                     json.loads(response.data))

    def test_list_items(self):
        with self.app() as client:
            with self.app_context():

                client.post("/store/Test_store_1")
                client.post("/item/Test_item", data={"price": 5.19, "store_id": 1})

                response = client.get("/items")

                self.assertDictEqual({'items': [{
                                                'name': 'Test_item',
                                                'price': 5.19
                                                }]
                                     }, json.loads(response.data))