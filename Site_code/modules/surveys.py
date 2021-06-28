import flask
import datetime

from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, request, make_response, Blueprint
from models.survey import Survey
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

@surveys.route('/get_survey/<id>', methods=['GET'])
#@login_required
def get_survey(id):
    qry = Session().query(Survey).filter_by(id=id)
    mys = None
    for row in qry :
        mys = {id : (row.id,row.permit_anon_answer,row.title,row.author_id)}
    return mys

@surveys.route('/get_survey', methods=['GET'])
#@login_required
def get_survey_all():
    qry = Session().query(Survey)
    mys = None
    for row in qry:
        mys += {id: (row.id, row.permit_anon_answer, row.title, row.author_id)}
    return mys

@surveys.route('/insert_survey', methods=['POST'])
def insert_survey():
    data = request.form
    return data