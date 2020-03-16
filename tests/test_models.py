"""
Test cases for <your resource name> Model

"""
import logging
import unittest
import os
from service import app
from service.models import Inventory, DataValidationError, db

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
##  INVENTORY   M O D E L   T E S T   C A S E S
######################################################################
class TestInventory(unittest.TestCase):
    """ Test Cases for <your resource name> Model """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
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

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()
        

######################################################################
#  P L A C E   T E S T   C A S E S   H E R E 
######################################################################

    def test_XXXX(self):
        """ Test something """
        self.assertTrue(True)
