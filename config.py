"""
Global Configuration for Application
"""
import os
import json
import platform

# Get configuration from environment
DATABASE_URI = os.getenv("DATABASE_URI", 
    "postgres://postgres:postgres@localhost:5432/postgres")

if platform.system() != 'Linux':
    fil = open("env\db.txt", "r") 
    DATABASE_URI = fil.read()

#override for cloud foundry
if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.environ['VCAP_SERVICES'])
    DATABASE_URI = vcap['user-provided'][0]['credentials']['url']

# Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Secret for session management
SECRET_KEY = os.getenv("SECRET_KEY", "s3cr3t-key-shhhh")
