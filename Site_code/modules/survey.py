import flask
from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, request, make_response, Blueprint, flash
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
def answer(id):
    s = Session().query(Survey).get(id)
    if s is None:
        return flask.Response(status=404)
    else:
        qs = sorted(s.questions, key=lambda x: x.order)
        for q in qs:
            if q.get_type() == QuestionTypes.OpenQuestion:
                q.open = q.open_question
            elif q.get_type() == QuestionTypes.ClosedQuestion:
                q.closed = q.closed_question
                q.closed.options = sorted(q.closed.closed_question_options, key=lambda x: x.order)
            else:
                pass  # TODO exception
        if not s.permit_anon_answer:
            @login_required
            def f():
                return render_template("surveys/answer.html", survey=s, questions=qs, QuestionTypes=QuestionTypes)
            return f()
        else:
            def f():
                return render_template("surveys/answer.html", survey=s, questions=qs, QuestionTypes=QuestionTypes)
            return f()


@survey.route('/<id>/', methods=['GET'])
# @login_required
def get_survey(id):
    s = Session().query(Survey).get(id)
    if s is None:
        return flask.Response(status=404)
    else:
        return json.dumps({"permit_anon_answer": s.permit_anon_answer, "title:": s.title, "author_id": s.author_id})


@survey.route('/', methods=['GET'])
# @login_required
def get_survey_all():
    qry = Session().query(Survey)
    data = {}
    for row in qry:
        data[row.id] = {"permit_anon_answer": row.permit_anon_answer, "title": row.title, "author_id": row.author_id}
    return json.dumps(data)


@survey.route('/', methods=['POST'])
# @login_required
def insert_survey():
    data = request.json
    survey = Survey(title=data['title'],
                    permit_anon_answer=data['permit_anon_answer'],
                    author_id=current_user.get_id(),
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


@survey.route('/<id>/', methods=['DELETE'])
# @login_required
def delete_survey(id):
    session = Session()
    survey = session.query(Survey).get(id)
    if survey is None:
        return flask.Response(status=404)
    else:
        if current_user.get_id() == str(survey.author_id):
            session.query(Survey).filter_by(id=id).delete()
            session.commit()
            return flask.Response(status=200)
        else:
            return flask.Response(status=401)


@survey.route('<id>/summary_questions/', methods=['GET', 'POST'])
@login_required
def summary_questions(id):
    s = Session().query(Survey).get(id)
    if s is None:
        return flask.Response(status=404)
    qs = sorted(s.questions, key=lambda x: x.order)
    for q in qs:
        if q.get_type() == QuestionTypes.OpenQuestion:
            q.open = q.open_question
        elif q.get_type() == QuestionTypes.ClosedQuestion:
            q.closed = q.closed_question
            q.closed.options = sorted(q.closed.closed_question_options, key=lambda x: x.order)
        else:
            pass  # TODO exception
    return render_template("surveys/summary_survey.html", survey=s, questions=qs, QuestionTypes=QuestionTypes)