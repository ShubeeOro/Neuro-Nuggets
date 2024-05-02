import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from neuro_nuggets.models import Question, User
from flask_login import login_required, current_user
from neuro_nuggets.db import db
from flask import Blueprint, render_template, redirect, url_for, request, flash

play = Blueprint('play', __name__)

@play.route('/')
@login_required
def start_game():
    return render_template('pages/play.html')


