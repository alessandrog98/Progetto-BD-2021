from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, DDL, event
from sqlalchemy.orm import relationship

from context import SQLBase, Session

class AnswerTypes(Enum):
    OpenAnswer = 1
    ClosedAnswer = 2

class Answer(SQLBase):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="answers")

    survey_id = Column(Integer, ForeignKey("surveys.id"))
    survey = relationship("Survey", back_populates="answers")

    closed_answers = relationship("ClosedAnswer", back_populates="answer")
    open_answers = relationship("OpenAnswer", back_populates="answer")

    def get_type(self):
        if self.closed_answer is not None and self.open_answer is None:
            return AnswerTypes.ClosedAnswer
        elif self.closed_answer is None and self.open_answer is not None:
            return AnswerTypes.OpenAnswer
        else:
            return None  # TODO ExceptionAns

SameSurvey = DDL(
    'CREATE OR REPLACE FUNCTION same_survey()'
    'RETURNS TRIGGER as $same_S$'
    'BEGIN'
    '   IF (new.id IN (SELECT answer_id FROM answers_closed;)) THEN'
    '       IF (new.survey_id = (SELECT DISTINCT(q.survey_id)'
    '                            FROM questions AS q JOIN questions_closed_option AS qc ON q.id=qc.closed_question_id '
    '                                 JOIN answers_closed AS a ON a.closed_question_option_id=qc.id'
    '                            WHERE a.id = new.id;)) THEN'
    '           RETURN NEW;'
    '   ELSE IF (new.id IN (SELECT answer_id FROM answers_open;)) THEN'
    '       IF (new.survey_id = (SELECT DISTINCT(q.survey_id)'
    '                            FROM questions AS q JOIN answers_open AS a ON q.id = a.open_question_id'
    '                            WHERE a.id = new.id;) THEN'
    '           RETURN NEW;'
    '   END IF;'
    '   RETURN NULL;'
    'END'
    '$same_S$ LANGUAGE plpgsql')

trigger_SameSurvey = DDL(
    'DROP TRIGGER IF EXISTS TrigSameSurvey ON answers;'
    'CREATE TRIGGER TrigSameSurvey'
    'BEFORE INSERT ON answers'
    'FOR EACH STATEMENT '
    'EXECUTE PROCEDURE same_survey();'
        )

event.listen(Answer, 'before_insert', trigger_SameSurvey)