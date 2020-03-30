"""
Inventory API Service Test Suite

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
class TestInventoryServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db()

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
        db.drop_all()
        

#     Test for creation
    def _create_inventory(self, count):
        """ Factory method to create inventory in bulk """
        inventory= []
        for _ in range(count):
            test_inv_item = InventoryFactory()
            resp = self.app.post(
                "/inventory", json=test_inv_item.serialize(), content_type="application/json"
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test inventory"
            )
            new_inv_item = resp.get_json()
            test_inv_item.id = new_inv_item["id"]
            inventory.append(test_inv_item)
        return inventory


    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Inventory REST API Service")


    def test_get_inventory_list(self):
        """ Get a list of Inventory Items """
        self._create_inventory(5)
        resp = self.app.get("/inventory")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_inventory(self):
        """ Get a single Inventory item """
        # get the id of an inventory item
        test_inv_item = self._create_inventory(1)[0]
        resp = self.app.get(
            "/inventory/{}".format(test_inv_item.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_inv_item.name)
        # get the sku of the inventory item
        resp = self.app.get(
            "/inventory/{}".format(test_inv_item.sku), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_inv_item.name)
        


    def test_get_inventory_not_found(self):
        """ Get an Inventory Item thats not found """
        resp = self.app.get("/inventory/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_inventory(self):
        """ Create a new Inventory """
        test_inv_item = InventoryFactory()
        serialized_item = test_inv_item.serialize()
        resp = self.app.post(
            "/inventory", json=serialized_item, content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertTrue(location != None)
        # Check the data is correct
        new_item = resp.get_json()
        self.assertEqual(new_item["name"], test_inv_item.name, "Names do not match")
        self.assertEqual(
            new_item["quantity"], test_inv_item.quantity, "Quantity does not match"
        )
        self.assertEqual(
            new_item["restockLevel"], test_inv_item.restockLevel, "Categories do not match"
        )
        # Check that the location header was correct
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_item = resp.get_json()
        self.assertEqual(new_item["name"], test_inv_item.name, "Names do not match")
        self.assertEqual(
            new_item["quantity"], test_inv_item.quantity, "Quantity does not match"
        )
        self.assertEqual(
            new_item["restockLevel"], test_inv_item.restockLevel, "Categories do not match"
        )

    def test_update_inventory(self):
        """ Update an existing inventory item"""
        #Create item to update
        test_inventory = InventoryFactory()
        resp = self.app.post(
            "/inventory", json=test_inventory.serialize(), content_type = "application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the inventory by sku
        new_item = resp.get_json()
        new_item['restockLevel'] = 20
        resp = self.app.put(
            "/inventory/{}".format(new_item['id']),
            json = new_item,
            content_type = "application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_inventory = resp.get_json()
        self.assertEqual(updated_inventory["restockLevel"], 20)

    def test_update_inventory_by_sku(self):
        """ Update an existing inventory item"""
        #Create item to update
        test_inventory = InventoryFactory()
        resp = self.app.post(
            "/inventory", json=test_inventory.serialize(), content_type = "application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the inventory by sku
        new_item = resp.get_json()
        new_item['restockLevel'] = 20
        resp = self.app.put(
            "/inventory/{}".format(new_item['sku']),
            json = new_item,
            content_type = "application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_inventory = resp.get_json()
        self.assertEqual(updated_inventory["restockLevel"], 20)

    def test_delete_inventory_item(self):
        """ Delete an Inventory Item """
        test_item = self._create_inventory(1)[0]
        resp = self.app.delete(
            "/inventory/{}".format(test_item.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "/inventory/{}".format(test_item.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


    def test_query_understocked_inventory(self):
        """ Query Understocked Inventory """
        inventory = []
        inventory.append(Inventory(name = "Rolex Watch", sku= "R1232020", quantity = 10, restockLevel = 12).create())
        inventory.append(Inventory(name = "Cartier Watch", sku= "C1232020", quantity = 12, restockLevel = 6).create())
        inventory.append(Inventory(name = "Tissot Watch", sku= "T1232020", quantity = 12).create())

        resp = self.app.get("/inventory/restock")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        inv_item = Inventory()
        inv_item.deserialize(data)
        self.assertEqual(inv_item.name, "Rolex Watch")
