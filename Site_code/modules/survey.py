import flask
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

survey = Blueprint('survey', __name__)


@survey.route('/new/', methods=['GET'])
@login_required
def new():
    return render_template("surveys/new.html")


@survey.route('/<id>/answer/', methods=['GET', 'POST'])
@login_required
def answer(id):
    s = Session().query(Survey).filter_by(id=id).first()
    return render_template("surveys/answer.html", survey=s, QuestionTypes=QuestionTypes)


@survey.route('/<id>/', methods=['GET'])
# @login_required
def get_survey(id):
    row = Session().query(Survey).filter_by(id=id).first()
    return json.dumps({"permit_anon_answer": row.permit_anon_answer, "title:": row.title, "author_id": row.author_id})


@survey.route('/', methods=['GET'])
# @login_required
def get_survey_all():
    qry = Session().query(Survey)
    data = {}
    for row in qry:
        data[row.id] = {"permit_anon_answer": row.permit_anon_answer, "title": row.title, "author_id": row.author_id}
    return json.dumps(data)


@survey.route('/', methods=['POST'])
def insert_survey():
    data = request.json
    survey = Survey(title=data['title'],
                    permit_anon_answer=data['permit_anon_answer'],
                    author_id=User.get_by_email('admin').id,
                    questions=[])
    for question_row in data['questions']:
        question = Question(order=question_row['order'],
                            title=question_row['title'],
                            text=question_row['text'])
        if question_row['type'] == str(QuestionTypes.OpenQuestion.value):
            question.open_question = OpenQuestion(regex=question_row['regex'],
                                                  regex_description=question_row['regex_description'],
                                                  mandatory=question_row['mandatory'])
        elif question_row['type'] == str(QuestionTypes.ClosedQuestion.value):
            question.closed_question = ClosedQuestion(min_n_of_answer=question_row['min'],
                                                      max_n_of_answer=question_row['max'])
            for option_row in question_row['options']:
                question.closed_question.closed_question_options.append(
                    ClosedQuestionOption(order=option_row['order'], text=option_row['text'])
                )
        else:
            pass  # TODO Exception
        survey.questions.append(question)

    session = Session()
    session.add(survey)
    session.commit()
    return flask.Response(status=200)
