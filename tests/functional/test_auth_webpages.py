import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from flask_login import LoginManager
from flask import Flask
import os
from dotenv import load_dotenv
from api.models import db, User

from api.routes.auth import auth
from api.routes.play import play
from api.routes.main import main

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') # os.environ.get('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('POSTGRES_URL') # os.environ.get('POSTGRES_URL')

# Initialize Database
db.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# Blueprints
app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(main, url_prefix="/")
app.register_blueprint(play, url_prefix="/play")