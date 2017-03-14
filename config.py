#DATABASE SETTINGS
import os

DEBUG = True
PORT = 8081
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = True
SECRET_KEY = "s0me random string"
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
