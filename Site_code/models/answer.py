from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, DDL, event
from sqlalchemy.orm import relationship

from context import SQLBase, Session
from .utils import denyUpdate


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
    denyUpdate(connection, Answer.__tablename__)

    connection.execute(""" 
            CREATE OR REPLACE FUNCTION same_survey()
            RETURNS TRIGGER as $$
            BEGIN
            IF EXISTS (
                SELECT *
                FROM answers_closed AS ac
                  INNER JOIN questions_closed_options AS qco ON ac.closed_question_option_id = qco.id
                  INNER JOIN questions AS q ON q.id = qco.closed_question_id
                WHERE ac.answer_id = NEW.id 
                    AND q.survey_id <> NEW.survey_id) 
                
            OR EXISTS (	
                SELECT *
                FROM answers_open AS ao
                INNER JOIN questions AS q ON q.id = ao.open_question_id
                WHERE ao.answer_id = NEW.id 
                    AND q.survey_id <> NEW.survey_id) THEN
                
                DELETE FROM answers WHERE id = NEW.id;
                
            END IF; 	
              
              RETURN NULL;
            END;
            $$ LANGUAGE plpgsql""")

    connection.execute("""
    CREATE OR REPLACE FUNCTION max_Ans() 
            RETURNS TRIGGER as $$
            DECLARE my_cursor refcursor;
            DECLARE idQ integer;
            DECLARE numAns integer;
            BEGIN
                   OPEN my_cursor FOR (SELECT DISTINCT qc.id
                                        FROM questions_closed AS qc
                                        INNER JOIN questions AS q ON q.id = qc.id
                                        WHERE q.survey_id = NEW.survey_id);
                   FETCH NEXT FROM my_cursor INTO idQ;
                   WHILE FOUND LOOP
                        numAns = (SELECT COUNT(*) FROM answers_closed WHERE closed_question_option_id = idQ AND answer_id = NEW.survey_id);
                        
                        IF (numAns > (SELECT q.max_n_of_answer 
                                    FROM questions_closed AS q
                                    WHERE q.id = idQ)
                        OR numAns < (SELECT q.min_n_of_answer
                                       FROM questions_closed AS q
                                       WHERE q.id = idQ)) THEN
                               
                            CLOSE my_cursor;
                            DELETE FROM answers WHERE id = NEW.id;
                            RETURN NULL;
                        END IF;
                        FETCH NEXT FROM my_cursor INTO idQ;
                   END LOOP;
                   CLOSE my_cursor;
                   RETURN NULL;
            END;
            $$ LANGUAGE plpgsql""")

    connection.execute("""
            DROP TRIGGER IF EXISTS TrigSameSurvey ON answers;
            CREATE TRIGGER TrigSameSurvey
            AFTER INSERT ON answers
            FOR EACH ROW
            EXECUTE PROCEDURE same_survey()""")

    connection.execute("""
            DROP TRIGGER IF EXISTS TrigMaxMinClosedAnswer ON answers;
            CREATE TRIGGER TrigMaxMinClosedAnswer
            AFTER INSERT ON answers
            FOR EACH ROW
            EXECUTE PROCEDURE max_Ans()""")
