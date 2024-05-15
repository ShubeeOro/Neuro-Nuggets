import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from flask import Flask, url_for, request, flash
import os
from dotenv import load_dotenv
from api.models import db, Question
import pytest

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') # os.environ.get('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('POSTGRES_URL') # os.environ.get('POSTGRES_URL')

# Initialize Database
db.init_app(app)

def test_homepage():
    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200

