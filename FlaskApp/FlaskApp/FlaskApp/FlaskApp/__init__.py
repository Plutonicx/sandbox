"""
The flask application package.
"""

from flask import Flask
from flask.ext.mysql import MySQL
app = Flask(__name__)


import FlaskApp.views
