"""
Inventory Service

Allows interaction with inventory system
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Inventory, DataValidationError

# Import Flask application
from . import app

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)

# def request_validation_error(error):
#     """ Handles Value Errors from bad data """
#     return bad_request(error)


# @app.errorhandler(status.HTTP_400_BAD_REQUEST)
# def bad_request(error):
#     """ Handles bad reuests with 400_BAD_REQUEST """
#     message = str(error)
#     app.logger.warning(message)
#     return (
#         jsonify(
#             status=status.HTTP_400_BAD_REQUEST, error="Bad Request", message=message
#         ),
#         status.HTTP_400_BAD_REQUEST,
#     )


# @app.errorhandler(status.HTTP_404_NOT_FOUND)
# def not_found(error):
#     """ Handles resources not found with 404_NOT_FOUND """
#     message = str(error)
#     app.logger.warning(message)
#     return (
#         jsonify(status=status.HTTP_404_NOT_FOUND, error="Not Found", message=message),
#         status.HTTP_404_NOT_FOUND,
#     )


# @app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
# def method_not_supported(error):
#     """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
#     message = str(error)
#     app.logger.warning(message)
#     return (
#         jsonify(
#             status=status.HTTP_405_METHOD_NOT_ALLOWED,
#             error="Method not Allowed",
#             message=message,
#         ),
#         status.HTTP_405_METHOD_NOT_ALLOWED,
#     )


# @app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
# def mediatype_not_supported(error):
#     """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
#     message = str(error)
#     app.logger.warning(message)
#     return (
#         jsonify(
#             status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#             error="Unsupported media type",
#             message=message,
#         ),
#         status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#     )


# @app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
# def internal_server_error(error):
#     """ Handles unexpected server error with 500_SERVER_ERROR """
#     message = str(error)
#     app.logger.error(message)
#     return (
#         jsonify(
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             error="Internal Server Error",
#             message=message,
#         ),
#         status.HTTP_500_INTERNAL_SERVER_ERROR,
#     )

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    #return (
    #    jsonify(
    #        name="Inventory REST API Service",
    #        version="1.0",
    #        paths=url_for("list_inventory", _external=True),
    #    ),
    #    status.HTTP_200_OK,
    #)
    return app.send_static_file('index.html')

######################################################################
# LIST ALL INVENTORY
######################################################################
@app.route("/inventory", methods=["GET"])
def list_inventory():
    """ Returns entire Inventory """
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
# RETRIEVE AN INVENTORY ITEM BY ID
######################################################################
@app.route("/inventory/<int:inv_id>", methods=["GET"])
def get_inventory_item_by_id(inv_id):
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
def get_inventory_item_by_sku(inv_sku):
    """
    Retrieve a record for single Inventory row

    This endpoint will return an Inventory row based on its sku
    """
    app.logger.info("Request for Item with sku: %", inv_sku)
    inv = Inventory.find_by_sku(inv_sku)[0]
    if not inv:
        raise NotFound("Inventory Item with sku '{}' was not found.".format(inv_sku))
    return make_response(jsonify(inv.serialize()), status.HTTP_200_OK)

######################################################################
# RETRIEVE OUT OF STOCK INVENTORY ITEMS 
# ######################################################################
@app.route("/inventory/restock", methods=["GET"])
def get_understocked_inventory():
    """
    Retrieve records that are out of stock

    """
    app.logger.info("Request for understocked inventory")
    inv = Inventory.find_understocked()
    if not inv:
        raise NotFound("Understocked Inventory was not found.")
    return make_response(jsonify(inv[0].serialize()), status.HTTP_200_OK)

######################################################################
# ADD A NEW INVENTORY ITEM
######################################################################
@app.route("/inventory", methods=["POST"])
def create_inventory():
    """
    Creates an Inventory Item
    This endpoint will create an Inventory Item based the data in the body that is posted
    """
    app.logger.info("Request to create inventory")
    check_content_type("application/json")
    inv = Inventory()
    inv.deserialize(request.get_json())
    inv.create()
    message = inv.serialize()
    location_url = url_for("get_inventory_item_by_id", inv_id=inv.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )



######################################################################
# UPDATE AN EXISTING INVENTORY ITEM
######################################################################
@app.route("/inventory/<int:inv_id>", methods=["PUT"])
def update_inventory(inv_id):
    """
    Update an inventory item

    This endpoint will update an inventory item based on the body that is posted
    """
    app.logger.info("Request to update inventory with id: %s", inv_id)
    check_content_type("application/json")
    inventory = Inventory.find(inv_id)
    update_item = inventory.deserialize(request.get_json())

    if not inventory:
        raise NotFound("Inventory with id '{}' was not found.".format(inv_id))
    inventory.name = update_item.name 
    inventory.sku = update_item.sku
    inventory.quantity = update_item.quantity
    inventory.restockLevel = update_item.restockLevel
    inventory.save()
    return make_response(jsonify(inventory.serialize()), status.HTTP_200_OK)

######################################################################
# UPDATE AN EXISTING INVENTORY ITEM BY SKU
######################################################################
@app.route("/inventory/<string:inv_sku>", methods=["PUT"])
def update_inventory_by_sku(inv_sku):
    """
    Update an inventory item

    This endpoint will update an inventory item based on the body that is posted
    """
    app.logger.info("Request to update inventory with sku: %s", inv_sku)
    check_content_type("application/json")
    inventory = Inventory.find_by_sku(inv_sku)[0]
    update_item = inventory.deserialize(request.get_json())

    if not inventory:
        raise NotFound("Inventory with sku '{}' was not found.".format(inv_sku))
    inventory.name = update_item.name 
    inventory.sku = update_item.sku
    inventory.quantity = update_item.quantity
    inventory.restockLevel = update_item.restockLevel
    inventory.save()
    return make_response(jsonify(inventory.serialize()), status.HTTP_200_OK)

######################################################################
# DELETE AN INVENTORY ITEM BY ID
######################################################################
@app.route("/inventory/<int:inv_id>", methods=["DELETE"])
def delete_inventory_item_by_id(inv_id):

    """
    Delete an Inventory Item

    This endpoint will delete and inventory item based the id specified in the path
    """
    app.logger.info("Request to delete inventory item with id: ", inv_id)
    inv = Inventory.find(inv_id)
    if inv:
        inv.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
# DELETE AN INVENTORY ITEM BY SKU
######################################################################
@app.route("/inventory/<string:inv_sku>", methods=["DELETE"])
def delete_inventory_item_by_sku(inv_sku):

    """
    Delete an Inventory Item

    This endpoint will delete and inventory item based the sku specified in the path
    """
    app.logger.info("Request to delete inventory item with sku: ", inv_sku)
    inv = Inventory.find_by_sku(inv_sku)
    if inv:
        inv.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)



######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Inventory.init_db(app)

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers["Content-Type"] == content_type:
        return
    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(415, "Content-Type must be {}".format(content_type))
