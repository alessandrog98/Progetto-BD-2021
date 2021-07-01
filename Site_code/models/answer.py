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

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    user = relationship("User", back_populates="answers")

    survey_id = Column(Integer, ForeignKey("surveys.id", ondelete="CASCADE"))
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

@event.listens_for(Answer.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    connection.execute(
    """CREATE OR REPLACE FUNCTION same_survey()
    RETURNS TRIGGER as $$
    BEGIN
       IF (new.id IN (SELECT answer_id FROM answers_closed)) THEN
           IF (new.survey_id = (SELECT q.survey_id
                                FROM answers_closed AS ac
                                INNER JOIN question_closed_option AS qco ON ac.closed_question_option_id = qco.id
                                INNER JOIN question AS q ON q.id = qco.closed_question_id
                                WHERE ac.id = new.id)) THEN
               RETURN NEW;
       ELSE IF (new.id IN (SELECT answer_id FROM answers_open)) THEN
           IF (new.survey_id = (SELECT q.survey_id
                                FROM answer_open AS ao
                                INNER JOIN question AS q ON ao.open_question_id = q.id
                                WHERE ao.id = new.id)) THEN
               RETURN NEW;
       END IF;
       RETURN NULL;
    END;
    $$ LANGUAGE plpgsql""")

trigger_SameSurvey = DDL(
    """DROP TRIGGER IF EXISTS TrigSameSurvey ON answers;
    CREATE TRIGGER TrigSameSurvey
    BEFORE INSERT OR UPDATE ON answers
    FOR EACH ROW
    EXECUTE PROCEDURE same_survey()""")

#event.listen(Answer, 'before_insert', trigger_SameSurvey)