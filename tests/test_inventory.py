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
    """ Test Cases for Inventory Model """

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
        db.drop_all()
        db.create_all()
        pass

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()
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

    def test_add_an_inventory_item(self):
        """ Create an inventory item and add it to the database """
        inventory = Inventory.all()
        self.assertEqual(inventory, [])
        inv_item = Inventory(name = "Rolex Watch", sku= "R1232020", quantity = 10, restockLevel = 12)
        self.assertTrue(inv_item != None)
        self.assertEqual(inv_item.id, None)
        inv_item.create()
        self.assertEqual(inv_item.id, 1)
        inventory = Inventory.all()
        self.assertEqual(len(inventory), 1)


    def test_delete_an_inventory_item(self):
        """ Delete an item """
        inv_item = InventoryFactory()
        inv_item.create()
        self.assertEqual(len(Inventory.all()), 1)
        inv_item.delete()
        self.assertEqual(len(Inventory.all()), 0)
    
    def test_serialize_an_inventory_item(self):
        """ Test serialization of an inventory item """
        inv_item = Inventory()
        data = inv_item.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], inv_item.id)
        self.assertIn("name", data )
        self.assertEqual(data["name"], inv_item.name)
        self.assertIn("sku", data )
        self.assertEqual(data["sku"], inv_item.sku)
        self.assertIn("quantity", data )
        self.assertEqual(data["quantity"], inv_item.quantity)
        self.assertIn("restockLevel", data )
        self.assertEqual(data["restockLevel"], inv_item.restockLevel)

    def test_deserialize_an_inventory_item(self):
        """ Test deserialization of an Inventory Item """
        data = {"id": 1, "name": "Rolex", "sku": "Rol1232020", "quantity":20, "restockLevel": 10}
        inv_item = Inventory()
        inv_item.deserialize(data)
        self.assertNotEqual(inv_item, None)
        self.assertEqual(inv_item.id, None)
        self.assertEqual(inv_item.name, "Rolex")
        self.assertEqual(inv_item.sku, "Rol1232020")
        self.assertEqual(inv_item.quantity, 20)
        self.assertEqual(inv_item.restockLevel, 10)


    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        inv_item = Inventory()
        self.assertRaises(DataValidationError, inv_item.deserialize, data)

    def test_find_item(self):
        """ Find an item by ID """
        inv_items = InventoryFactory.create_batch(3)
        for inv_item in inv_items:
            inv_item.create()
        logging.debug(inv_items)
        # make sure they got saved
        self.assertEqual(len(Inventory.all()), 3)
        # find the 2nd inventory item in the list
        inv_item = Inventory.find(inv_items[1].id)
        self.assertIsNot(inv_item, None)
        self.assertEqual(inv_item.id, inv_items[1].id)
        self.assertEqual(inv_item.name, inv_items[1].name)
        self.assertEqual(inv_item.sku, inv_items[1].sku)

    def test_find_by_sku(self):
        """ Find Inventory items by sku """
        Inventory(name = "Rolex Watch", sku= "R1232020", quantity = 10, restockLevel = 12).create()
        Inventory(name = "Cartier Watch", sku= "C1232020", quantity = 12, restockLevel = 6).create()
        inv_items = Inventory.find_by_sku("R1232020")
        self.assertEqual(inv_items[0].name, "Rolex Watch" )
        self.assertEqual(inv_items[0].quantity, 10)
        self.assertEqual(inv_items[0].restockLevel, 12)

    def test_find_by_name(self):
        """ Find Inventory items by name """
        Inventory(name = "Rolex Watch", sku= "R1232020", quantity = 10, restockLevel = 12).create()
        Inventory(name = "Cartier Watch", sku= "C1232020", quantity = 12, restockLevel = 6).create()
        inv_items = Inventory.find_by_name("Cartier Watch")
        self.assertEqual(inv_items[0].sku, "C1232020" )
        self.assertEqual(inv_items[0].quantity, 12)
        self.assertEqual(inv_items[0].restockLevel, 6)

    def test_find_or_404_found(self):
        """ Find or return 404 found """
        inv_items = InventoryFactory.create_batch(3)
        for inv_item in inv_items:
            inv_item.create()

        inv_item = Inventory.find_or_404(inv_items[1].id)
        self.assertIsNot(inv_item, None)
        self.assertEqual(inv_item.id, inv_items[1].id)
        self.assertEqual(inv_item.name, inv_items[1].name)
        self.assertEqual(inv_item.quantity, inv_items[1].quantity)
        self.assertEqual(inv_item.sku, inv_items[1].sku)

    def test_find_or_404_not_found(self):
        """ Find or return 404 NOT found """
        self.assertRaises(NotFound, Inventory.find_or_404, 0)
