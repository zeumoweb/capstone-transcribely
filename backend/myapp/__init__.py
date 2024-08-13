from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from pymongo import MongoClient


USERNAME = # Mongo Username
PASSWORD = # Password
URL = # URL


app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

def mongo_conn():
    """create a connection"""
    try:
        conn = MongoClient(URL, port=27017)
        db = conn.transcribely
        return db
    except Exception as err:
        print(f"Error in mongodb connection: {err}")


db = mongo_conn()

from myapp import routes