from api.index import db, Question, User
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash

play = Blueprint('play', __name__)

@play.route('/')
@login_required
def start_game():
    return render_template('pages/game_mode.html')

@play.route('/endless')
@login_required
def endless_game():
    return render_template('pages/endless.html')

@play.route('/solo')
@login_required
def solo_game():
    return render_template('pages/solo.html')
