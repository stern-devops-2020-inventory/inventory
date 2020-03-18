"""
<your resource name> API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from flask_api import status  # HTTP Status Codes
from service.models import Inventory, DataValidationError, db
from .factories import InventoryFactory
from service.service import app, init_db

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  T E S T   C A S E S
######################################################################
class TestInventory(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db()
        pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """Runs before each test"""
        db.drop_all()
        db.create_all()
        self.app = app.test_client()


    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        pass

    #Update test
    def test_update_inventory(self):
        """ Update an existing inventory item"""
        #Create item to update
        test_inventory = InventoryFactory()
        resp = self.app.post(
            "/inventory", json=test_inventory.serialize(), content_type = "application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the inventory
        new_inventoryitem = resp.get_json()
        new_inventoryitem['restockLevel'] = 20
        resp = self.app.put(
            "/inventory/{}".format(new_inventoryitem['sku']),
            json = new_inventoryitem,
            content_type = "application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_inventory = resp.get_json()
        self.assertEqual(updated_inventory["restockLevel"], 20)

######################################################################
#  P L A C E   T E S T   C A S E S   H E R E 
######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
