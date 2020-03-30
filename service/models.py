"""
Models for Inventory

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Inventory(db.Model):
    """
    Class that represents Inventory
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    sku = db.Column(db.String(63)) 
    quantity = db.Column(db.Integer)
    restockLevel = db.Column(db.Integer) # OPTIONAL Level at which we will need to restock the item.

    def __repr__(self):
        return "Product %r sku %r id=[%s]>" % (self.name, self.sku, self.id)

    def create(self):
        """
        Creates Inventory to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates Inventory to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes Inventory from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes Inventory into a dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "quantity": self.quantity,
            "restockLevel": self.restockLevel
        }

    def deserialize(self, data):
        """
        Deserializes Inventory from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.sku = data["sku"]
            self.quantity = data["quantity"]
            self.restockLevel = data["restockLevel"]
        except KeyError as error:
            raise DataValidationError("Invalid <your resource name>: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid inventory: body of request contained" "bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the <your resource name>s in the database """
        logger.info("Processing all Inventories")
        return cls.query.all()

    @classmethod
    def find(cls, inv_id):
        """ Finds Inventory by it's ID """
        logger.info("Processing lookup for id %s ...", inv_id)
        return cls.query.get(inv_id)

    @classmethod
    def find_by_sku(cls, sku):
        """ Finds Inventory by it's sku """
        logger.info("Processing lookup for sku %s ...", sku)
        return cls.query.filter(cls.sku == sku)

    @classmethod
    def find_or_404(cls, inv_id):
        """ Find Inventory by it's id """
        logger.info("Processing lookup or 404 for id %s ...", inv_id)
        return cls.query.get_or_404(inv_id)

    @classmethod
    def find_by_name(cls, name):
        """ Returns all <your resource name>s with the given name

        Args:
            name (string): the name of the <your resource name>s you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_understocked(cls):
    #Return items that are understocked
        return cls.query.filter(cls.quantity < cls.restockLevel)

        