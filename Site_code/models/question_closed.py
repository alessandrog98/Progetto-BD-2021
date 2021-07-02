from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, Text, CheckConstraint, event
from sqlalchemy.orm import relationship

from context import SQLBase, Session
from .utils import denyUpdate


class ClosedQuestion(SQLBase):
    __tablename__ = 'questions_closed'
    __table_args__ = (
        CheckConstraint('min_n_of_answer >= 0'),
        CheckConstraint('max_n_of_answer > 0'),
        CheckConstraint('max_n_of_answer >= min_n_of_answer')
    )

    id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True)
    question = relationship("Question", back_populates="closed_question")

    min_n_of_answer = Column(Integer)
    max_n_of_answer = Column(Integer)

    closed_question_options = relationship("ClosedQuestionOption", back_populates="closed_question")


@event.listens_for(ClosedQuestion.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    denyUpdate(connection, ClosedQuestion.__tablename__)

    connection.execute("""
                CREATE OR REPLACE FUNCTION max_quest() 
                RETURNS TRIGGER as $$
                DECLARE numOpt integer;
                DECLARE idS integer;
                BEGIN
                    idS = (SELECT q.survey_id FROM questions AS q WHERE q.id = NEW.id) ;
                    numOpt = (SELECT COUNT(*) FROM questions_closed_options WHERE closed_question_id = NEW.id);
                    IF (NEW.min_n_of_answer >= numOpt OR NEW.max_n_of_answer >= numOpt) THEN
                        DELETE FROM surveys WHERE id = idS;
                    END IF;
                    RETURN NULL;
                END;
                $$ LANGUAGE plpgsql""")

    # connection.execute(""" # Need to be translated in after statement
    #             DROP TRIGGER IF EXISTS TrigMaxMinClosedQuestion ON questions_closed;
    #             CREATE TRIGGER TrigMaxMinClosedQuestion
    #             AFTER INSERT ON questions_closed
    #             FOR EACH ROW
    #             EXECUTE PROCEDURE max_quest()""")
