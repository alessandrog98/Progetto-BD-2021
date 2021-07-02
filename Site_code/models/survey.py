from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, CheckConstraint, event
from sqlalchemy.orm import relationship

from context import SQLBase, Session
from .utils import denyUpdate


class Survey(SQLBase):
    __tablename__ = 'surveys'
    __table_args__ = (
        CheckConstraint('LENGTH(title) > 0'),
    )

    id = Column(Integer, primary_key=True)
    permit_anon_answer = Column(Boolean)
    title = Column(String(250))

    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    author = relationship("User", back_populates="surveys")

    questions = relationship("Question", back_populates="survey")
    answers = relationship("Answer", back_populates="survey")


@event.listens_for(Survey.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    denyUpdate(connection, Survey.__tablename__)

    connection.execute(
        """ CREATE OR REPLACE FUNCTION HasQuestions()
            RETURNS TRIGGER as $$ 
            BEGIN
                IF (NOT EXISTS (SELECT q.*
                                FROM questions AS q
                                WHERE survey_id = new.id )) THEN 
                                DELETE FROM surveys
                                WHERE id = new.id;
                                RETURN NULL;
                END IF;
                RETURN NULL;
            END;
            $$ LANGUAGE plpgsql""")

    # connection.execute("""
    #             DROP TRIGGER IF EXISTS TrigHasQuestions ON surveys;
    #             CREATE TRIGGER TrigHasQuestions
    #             AFTER INSERT ON surveys
    #             FOR EACH ROW
    #             EXECUTE PROCEDURE HasQuestions()""")
