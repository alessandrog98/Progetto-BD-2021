import flask

from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, request, make_response, Blueprint

from context import Session
from models.users import User


front = Blueprint('front', __name__)


@front.route('/')
def home():
    return render_template("front/home.html")


@front.route('/reserved_area')
@login_required
def reserved_area():
    data = User.my_surveys(current_user.get_id())
    return render_template("front/reserved.html", data=data)

