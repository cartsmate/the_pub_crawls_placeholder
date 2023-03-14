import os
from configparser import ConfigParser
from flask import Flask

flask_app = Flask(__name__)

constants = ConfigParser()
constants.read(os.getcwd() + "/constants.ini")

from .views import flask_app
