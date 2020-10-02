"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.

"""

from unittest import TestCase
from app import app
from db import db

class BaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        # Make sure database exists - we crate a very basic data.db file, because it's harder to setup or delete a MySQL db
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'

        with app.app_context(): # loads all app config and variables (pretends to be a real app) so everything
                                # that interacts with the apps as the real app was running
            db.init_app(app)


    def setUp(self):

        with app.app_context():
            db.create_all()

        # Get a test client
        app.testing = True
        self.app = app.test_client
        self.app_context = app.app_context

        pass

    def tearDown(self):
        # Database gets blank
        with app.app_context():
            db.session.remove()
            db.drop_all()