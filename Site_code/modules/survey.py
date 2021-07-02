import tempfile

import flask
import xlsxwriter
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


@survey.route('/<id>/summary_questions/', methods=['GET', 'POST'])
@login_required
def summary_questions(id):
    s = Session().query(Survey).get(id)
    answers = {}
    if s is None:
        return flask.Response(status=404)
    if current_user.get_id() != str(s.author_id):
        return flask.Response(status=401)

    questions = sorted(s.questions, key=lambda x: x.order)
    for q in questions:
        if q.get_type() == QuestionTypes.OpenQuestion:
            q.open = q.open_question
            q.answers = []
            for oq in q.open_question.open_answers:
                q.answers.append(oq.text)
        elif q.get_type() == QuestionTypes.ClosedQuestion:
            q.closed = q.closed_question
            closed_options = sorted(q.closed_question.closed_question_options, key=lambda x: x.order)
            answers[q.id] = {}
            answers[q.id]['answer_type'] = 'closed'
            my_list = []
            for cqo in closed_options:
                my_list.append({cqo.text: len(cqo.closed_answers)})
            answers[q.id]['data'] = my_list
        else:
            pass  # TODO exception
    return render_template("surveys/summary_survey.html",
                           survey=s,
                           answer_count=len(s.answers),
                           questions=questions,
                           data=json.dumps(answers),
                           QuestionTypes=QuestionTypes)


@survey.route('/<id>/download/', methods=['GET', 'POST'])
@login_required
def summary_questions(id):
    s = Session().query(Survey).get(id)
    if s is None:
        return flask.Response(status=404)
    if current_user.get_id() != str(s.author_id):
        return flask.Response(status=401)

    with tempfile.TemporaryDirectory() as tmpdir:
        dir = tmpdir + '/ragazzi.xlsx'
        workbook = xlsxwriter.Workbook(dir)
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 0, 'ID')
        worksheet.write(0, 1, 'Cognome')
        worksheet.write(0, 2, 'Nome')
        worksheet.write(0, 3, 'Telefono')
        worksheet.write(0, 4, 'Telefono 2')
        worksheet.write(0, 5, 'Data Nascita')
        worksheet.write(0, 6, 'Paese')
        worksheet.write(0, 7, 'Indirizzo')
        worksheet.write(0, 8, 'Taglia')
        worksheet.write(0, 9, 'Quota')
        worksheet.write(0, 10, 'Anticipato')
        worksheet.write(0, 11, 'Posticipato')
        worksheet.write(0, 12, 'Laboratorio 1')
        worksheet.write(0, 13, 'Laboratorio 2')
        worksheet.write(0, 14, 'Laboratorio 3')
        worksheet.write(0, 15, 'Laboratorio 4')

        i = 2
        for ragazzo in queryset:
            worksheet.write(i, 0, str(ragazzo.pk))
            worksheet.write(i, 1, str(ragazzo.cognome))
            worksheet.write(i, 2, str(ragazzo.nome))
            if ragazzo.telefono is not None:
                worksheet.write(i, 3, str(ragazzo.telefono))
            if ragazzo.telefono_2 is not None:
                worksheet.write(i, 4, str(ragazzo.telefono_2))
            worksheet.write(i, 5, str(ragazzo.data_nascita))
            worksheet.write(i, 6, str(ragazzo.paese))
            worksheet.write(i, 7, str(ragazzo.indirizzo))
            worksheet.write(i, 8, str(ragazzo.taglia))
            worksheet.write(i, 9, str(ragazzo.quota))
            # if ragazzo.quota_anticipato is not None:
            worksheet.write(i, 10, ('Elementari' if ragazzo.quota_anticipato == 0 else 'Medie'))
            worksheet.write(i, 11, str(ragazzo.quota_posticipato))
            if ragazzo.laboratorio1 is not None:
                worksheet.write(i, 12, str(ragazzo.laboratorio1.nome))
            if ragazzo.laboratorio2 is not None:
                worksheet.write(i, 13, str(ragazzo.laboratorio2.nome))
            if ragazzo.laboratorio3 is not None:
                worksheet.write(i, 14, str(ragazzo.laboratorio3.nome))
            if ragazzo.laboratorio4 is not None:
                worksheet.write(i, 15, str(ragazzo.laboratorio4.nome))
            i += 1

        workbook.close()
        return download(request, dir)