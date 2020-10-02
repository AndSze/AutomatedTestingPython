from models.user import UserModel
from tests.system.system_base_test import BaseTest
import json

# json.dumps() -> converts a Python dictionary into JSON string
# json.loads() -> converts a JSON string into Python dictionary

class UserTest(BaseTest):

    def test_register_user(self):
        with self.app() as client:  # to make us able to make requests to test client app
            with self.app_context():

                response = client.post("/register", data = {"username": "test", "password": "1234"})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username("test"))
                self.assertDictEqual({"message": "User created successfully."},
                                      json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():

                # '/register', '/auth' <- endpoints on the web server side
                client.post("/register", data={"username": "test", "password": "1234"})

                # "Content-Type" tells a web server what kind of data we are sending to the server
                auth_response = client.post('/auth',
                                           data=json.dumps({"username": "test", "password": "1234"}),
                                           headers={"Content-Type": "application/json"})

                print(auth_response.data)
                self.assertIn("access_token", json.loads(auth_response.data).keys()) # ["access_token", ....]

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():

                client.post("/register", data={"username": "test", "password": "1234"})
                response = client.post("/register", data={"username": "test", "password": "1234"})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({"message": "A user with that username already exists"},
                                      json.loads(response.data))