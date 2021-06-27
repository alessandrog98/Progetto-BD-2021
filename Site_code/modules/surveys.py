import flask
import datetime

from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, request, make_response, Blueprint

from context import Session
from models.users import User

surveys = Blueprint('surveys', __name__)


@surveys.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    return render_template("surveys/new.html")


@surveys.route('/id/answer', methods=['GET', 'POST'])
# @login_required
def answer():
    return render_template("surveys/answer.html")


@surveys.route('/')
def home():
    return render_template("front/home.html")
