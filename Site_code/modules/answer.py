from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, request, make_response, Blueprint
from models.answer import Answer, AnswerTypes
from context import Session
from models.question import Question, QuestionTypes
from models.answer_closed import ClosedAnswer
from models.answer_open import OpenAnswer
from models.question_open import OpenQuestion
from models.survey import Survey
from models.question_closed_option import ClosedQuestionOption
import json

answer = Blueprint('answer', __name__)


@answer.route('/<id>/', methods=['GET'])
# @login_required
def get_answer(id):
    quest = Session().query(Question).get(id)
    data = {}
    if quest.get_type() == QuestionTypes.OpenQuestion:
        quest = Session().query(OpenQuestion).get(id)
        for ans in quest.answer:
            data[quest.id] = {ans.text}
        return json.dumps(data)
    elif quest.get_type() == QuestionTypes.ClosedQuestion:
        quest = Session().query(ClosedQuestionOption).filter_by(closed_question_id=id)
        all_q = []
        for q in quest:
            all_q.append(q)
        for ans in all_q:
            for an in ans.closed_answers:
                data[ans.id] = {an.answer_id}
        return json.dumps(data)
    else:
        pass


@answer.route('/answers_all/<id>/', methods=['GET'])
# @login_required
def get_answers_all(id):
    quest = Session().query(Question).filter_by(survey_id=id)
    data = {}
    for ans in quest:
        get_answer(ans.id)
    return


@answer.route('/', methods=['POST'])
# @login_required
def insert_answer():
    data = request.json
    session = Session()
    survey = session.query(Survey).get(data['survey_id'])
    answer = Answer(user_id=current_user.get_id())
    for answer_row in data['answers']:
        if answer_row['type'] == str(AnswerTypes.OpenAnswer.value):
            answer.open_answers.append(OpenAnswer(open_question_id=answer_row['open_question_id'], text=answer_row['text']))
        elif answer_row['type'] == str(AnswerTypes.ClosedAnswer.value):
            answer.closed_answers.append(ClosedAnswer(closed_question_option_id=answer_row['closed_question_option_id']))
        else:
            pass  # TODO Exception
    survey.answers.append(answer)
    session.commit()
    return data
