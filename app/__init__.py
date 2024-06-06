# app/__init__.py
from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Set up MongoDB connection
app.config[
    "MONGO_URI"] = "mongodb+srv://Ritik360:ritik810@cluster0.e1pgcys.mongodb.net/aspireit?retryWrites=true&w=majority&appName=Cluster0"

app.config["SECRET_KEY"] = "your_secret_key_here"

db = PyMongo(app).db
bcrypt = Bcrypt(app)

# Import routes (ensure this is at the end after app and mongo are defined)
from app import routes
