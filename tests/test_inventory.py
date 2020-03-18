"""
Test cases for Inventory Model

"""
import logging
import unittest
import os
from werkzeug.exceptions import NotFound
from service.models import Inventory, DataValidationError, db
from service import app
from .factories import InventoryFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  I N V E N T O R Y   M O D E L   T E S T   C A S E S
######################################################################
class TestInventoryModel (unittest.TestCase):
    """ Test Cases for <your resource name> Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Inventory.init_db(app)


    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        pass

    def tearDown(self):
        """ This runs after each test """
        pass

    def test_create_an_inventory_item(self):
        """ Create an intentory item and assert that it exists"""
        inv_item = Inventory(name = "Rolex Watch", sku= "R1232020", quantity = 10, restockLevel = 12)
        self.assertTrue(inv_item != None)
        self.assertEqual(inv_item.id, None)
        self.assertEqual(inv_item.name, "Rolex Watch")
        self.assertEqual(inv_item.sku, "R1232020")
        self.assertEqual(inv_item.quantity, 10)
        self.assertEqual(inv_item.restockLevel, 12)

######################################################################
#  P L A C E   T E S T   C A S E S   H E R E 
######################################################################

    def test_XXXX(self):
        """ Test something """
        self.assertTrue(True)
