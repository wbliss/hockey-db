
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import (
    HOCKEY_DB,
    SECRET_KEY
)


app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = HOCKEY_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = SECRET_KEY


