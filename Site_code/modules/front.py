import flask
import datetime

from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, request, make_response, Blueprint

from context import Session
from models.users import User


front = Blueprint('front', __name__)


@front.route('/private')
@login_required
def private():
    users = current_user.get_id()
    resp = make_response(render_template("private.html", users=users))
    return resp


@front.route('/')
def home():
    return render_template("front/home.html")

