# inventory

# nyu-travis-ci badge
[![Build Status](https://travis-ci.org/stern-devops-2020-inventory/inventory.svg?branch=master)](https://travis-ci.org/stern-devops-2020-inventory/inventory)
[![Codecov](https://img.shields.io/codecov/c/github/nyu-devops/lab-travis-ci.svg)]()
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# overview
The inventory resource keeps track of how many of each product we have in our warehouse. At a minimum it should reference a product and the quantity on hand. Check with the Product team for the format of the product id. Inventory could also track restock levels and the condition of the item (i.e., new, open box, used). Restock levels will help you know when to order more products. Being able to query products by their condition (e.g., new, used) could be very useful.


Setup
To run this project, clone this repository and install vagrant virtual machine . Next, initialize a vagrant enviroment using vagrant up. Then do:

vagrant ssh
cd /vagrant
nosetests
honcho start

Attributes
The Inventory Model contains the following attributes:

"id"
"name"
"sku"
"quantity"
"restockLevel"

Functions
*coming soon*

What's Featured in the Project?
The project contains the following:

.github/            - contains a template for github issues
assets/             - contains image files

service/            - service python package
├── static/         - conatains web UI files
├── __init__.py     - package initializer
├── models.py       - module with business models
└── service.py      - module with service routes

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for busines models
└── test_service.py - test suite for service routes

.coveragerc         - settings file for code coverage options
.gitignore          - this will ignore vagrant and other metadata files
.travis.yml         - travis configuration file
LICENSE             - Apache 2.0
Procfile            - a command to run by the container
README.md           - repo documentation file
Vagrantfile         - Vagrant file that installs requirements to the VM
codecov.yml         - codecov configuration file
config.py           - configuration parameters
dot-env-example     - copy to .env to use environment variables
manifest.yml        - ibm cloud foundry configuration file
requirements.txt    - list if Python libraries required by your code
runtime.txt         - python version to be used at runtime
setup.cfg           - nosetests configuration file

Running the Tests
Run the tests using nosetests and coverage

$ nosetests
$ coverage report -m --include=server.py
Nose is configured to automatically include the flags --rednose --with-spec --spec-color --with-coverage so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

