from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, request, make_response, Blueprint
from models.answer import Answer, AnswerTypes
from context import Session
from models.users import User
from models.question import Question, QuestionTypes
from models.answer_closed import ClosedAnswer
from models.answer_open import OpenAnswer
from models.question_open import OpenQuestion
from models.survey import Survey
from models.question_closed_option import ClosedQuestionOption
import json

answers = Blueprint('answer', __name__)


@answers.route('/answers/<id>', methods=['GET'])
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
        for q in quest :
            all_q.append(q)
        for ans in all_q:
            for an in ans.closed_answers:
                data[ans.id] = {an.answer_id}
        return json.dumps(data)
    else:
        pass

@answers.route('/answers_all/<id>', methods=['GET'])
# @login_required
def get_answers_all(id):
    quest = Session().query(Question).filter_by(survey_id=id)
    data = {}
    for ans in quest:
        get_answer(ans.id)
    return

@answers.route('/answers/<id>', methods=['POST'])
# @login_required
def insert_answer(id):
    data = request.json
    survey = Session().query(Survey).filter_by(id=id)

    for answer_row in data['answers']:
        answer = Answer(user_id= current_user.id if current_user is None else None,
                        survey_id=id)
        if answer_row['type'] == str(AnswerTypes.OpenAnswer.value):
            answer.open_answers = OpenAnswer(text=answer_row['text'])
        elif answer_row['type'] == str(AnswerTypes.ClosedAnswer.value):
            answer.closed_answers = ClosedAnswer(closed_question_option_id = answer_row['closed_question_option_id'])
        else:
            pass  # TODO Exception
    survey.answers.insert(answer)
    session = Session()
    session.commit()
    return data

