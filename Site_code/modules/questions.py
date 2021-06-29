from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, request, make_response, Blueprint
from models.answer import Answer
from context import Session
from models.users import User
from models.question import Question, QuestionTypes
from models.question_open import OpenQuestion
from models.question_closed import ClosedQuestion
from models.question_closed_option import ClosedQuestionOption
import json


questions = Blueprint('questions', __name__)


@questions.route('/questions/<id>', methods=['GET'])
# @login_required
def get_answer(id):
    quest = Session().query(Question).filter_by(id=id)
    data = {}
    if quest.get_type == QuestionTypes.OpenQuestion:
        quest = Session().query(OpenQuestion).filter_by(id=id)
        for ans in quest.open_answer:
            data[quest.id] = {ans.text}
        return json.dumps(data)
    elif quest.get_type == QuestionTypes.ClosedQuestion:
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


@questions.route('/questions/<id>', methods=['GET'])
# @login_required
def get_answers_all(id):
    quest = Session().query(Question).filter_by(survey_id=id)
    data = {}
    for ans in quest:
        get_answer(ans.id)
    return

