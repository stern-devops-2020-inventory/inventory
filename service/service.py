"""
My Service

Describe what your service does here
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Inventory, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return "Reminder: return some useful information in json format about the service here", status.HTTP_200_OK


######################################################################
# LIST ALL INVENTORY
######################################################################
@app.route("/inventory", methods=["GET"])
def list_inventory():
    """ Returns entire list of Inventory items """
    app.logger.info("Request for entire inventory")
    inventory = []
    sku = request.args.get("sku")
    name = request.args.get("name")
    if sku:
        inventory = Inventory.find_by_sku(sku)
    elif name:
        inventory = Inventory.find_by_name(name)
    else:
        inventory = Inventory.all()

    results = [inv.serialize() for inv in inventory]
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# ADD NEW INVENTORY
######################################################################
@app.route("/inventory", methods = ["POST"])
def create_inventory(self, count):
    """
    Creates New Inventory
    This endpoint will create inventory based the data in the body that is posted
    """
    app.logger.info ("Request to create inventory")
    check_content_type("application/json")
    inv_item = Inventory()
    inv_item.deserialize(request.get_json())
    inv_item.create()
    message = inv_item.serialize()
    location_url = url_for("list_inventory", sku=inv_item.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
# UPDATE AN EXISTING INVENTORY ITEM
######################################################################
@app.route("/")
def update_inventory():
    """
    Update an inventory item

    This endpoint will update an inventory item based on the body that is posted
    """
    app.logger.info("Request to update inventory with sku: %s", sku)
    check_content_type("application/json")
    inventory = Inventory.find_by_sku(sku)
    if not inventory:
        raise NotFound("Inventory with sku '{}' was not found.".format(sku))
    inventory.deserialize(request.get_json())
    inventory.sku = sku 
    inventory.save()
    return make_response(jsonify(inventory.serialize()), status.HTTP_200_OK)


######################################################################
# RETRIEVE AN INVENTORY ITEM BY ID
######################################################################
@app.route("/inventory/<int:inv_id>", methods=["GET"])
def get_inventory_item(inv_id):
    """
    Retrieve a record for single Inventory row
    This endpoint will return an Inventory row based on its id
    """
    app.logger.info("Request for pet with id: %", inv_id)
    inv = Inventory.find(inv_id)
    if not inv:
        raise NotFound("Inventory Item with id '{}' was not found.".format(inv_id))
    return make_response(jsonify(inv.serialize()), status.HTTP_200_OK)
######################################################################
# RETRIEVE AN INVENTORY ITEM BY SKU
######################################################################
@app.route("/inventory/<string:inv_sku>", methods=["GET"])
def get_inventory_item(inv_sku):
    """
    Retrieve a record for single Inventory row
    This endpoint will return an Inventory row based on its sku
    """
    app.logger.info("Request for pet with sku: %", inv_sku)
    inv = Inventory.find_by_sku(inv_sku)
    if not inv:
        raise NotFound("Inventory Item with sku '{}' was not found.".format(inv_sku))
    return make_response(jsonify(inv.serialize()), status.HTTP_200_OK)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Inventory.init_db(app)



