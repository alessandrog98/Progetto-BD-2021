from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, request, make_response, Blueprint
from models.survey import Survey
from context import Session
from models.users import User
from models.question import Question, QuestionTypes
from models.question_open import OpenQuestion
from models.question_closed import ClosedQuestion
from models.question_closed_option import ClosedQuestionOption
import json


answers = Blueprint('answer', __name__)

@answers.route('/answers/<id>', methods=['GET'])
# @login_required
def get_answer(id):
    qry = Session().query().filter_by(id=id)
    mys = None
    for row in qry :
        mys = {id : (row.id ,row.permit_anon_answer ,row.title ,row.author_id)}
    return mys


@answers.route('/survey', methods=['GET'])
# @login_required
def get_survey_all():
    qry = Session().query(Survey)
    data = {}
    for row in qry:
        data[row.id] = {(row.permit_anon_answer, row.title, row.author_id)}
    return data