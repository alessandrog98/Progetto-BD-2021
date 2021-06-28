
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

@surveys.route('/survey/<id>', methods=['GET'])
# @login_required
def get_survey(id):
    qry = Session().query(Survey).filter_by(id=id)
    mys= {}
    for row in qry :
        mys[row.id] = {"permit_anon_answer":row.permit_anon_answer ,"title:":row.title ,"autor_id":row.author_id}
    return json.dumps(mys)

@surveys.route('/survey', methods=['GET'])
# @login_required
def get_survey_all():
    qry = Session().query(Survey)
    data = {}
    for row in qry:
        data[row.id] = {"permit_anon_answer":row.permit_anon_answer, "title":row.title, "author_id":row.author_id}
    return json.dumps(data)


@surveys.route('/survey', methods=['POST'])
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
        if question_row['type'] == QuestionTypes.OpenQuestion:
            question.open_question = OpenQuestion(regex=question_row['regex'],
                                                  regex_description=question_row['regex_description'],
                                                  mandatory=question_row['mandatory'])
        elif question_row['type'] == QuestionTypes.ClosedQuestion:
            question.closed_question = ClosedQuestion(min_n_of_answer=question_row['min'],
                                                      max_n_of_answer=question_row['max'])
            for option_row in question_row['options']:
                option = ClosedQuestionOption(order=question_row['order'],
                                              text=question_row['text'])
                question.closed_question.closed_question_options.insert(option)
        else:
            pass  # TODO Exception
    survey.questions.insert(question)
    session = Session()
    session.add(survey)
    session.commit()
    return data
