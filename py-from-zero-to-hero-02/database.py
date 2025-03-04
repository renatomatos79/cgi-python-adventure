from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Import the config class
from config import config_class

app = Flask(__name__)

# Load configurations from config.py
app.config.from_object(config_class)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)