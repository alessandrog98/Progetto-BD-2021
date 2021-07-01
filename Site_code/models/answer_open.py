from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, Text, event
from sqlalchemy.orm import relationship

from context import SQLBase, Session


class OpenAnswer(SQLBase):
    __tablename__ = 'answers_open'

    id = Column(Integer, primary_key=True)
    text = Column(Text)

    open_question_id = Column(Integer, ForeignKey("questions_open.id", ondelete="CASCADE"))
    open_question = relationship("OpenQuestion", back_populates="open_answers")

    answer_id = Column(Integer, ForeignKey("answers.id", ondelete="CASCADE"))
    answer = relationship("Answer", back_populates="open_answers")


@event.listens_for(OpenAnswer.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    connection.execute(
        """ CREATE OR REPLACE FUNCTION regex() 
            RETURNS TRIGGER as $$ 
            DECLARE 
                mandatory boolean;
                regex varchar;   
            BEGIN
                mandatory = (SELECT q.mandatory FROM questions_open AS q WHERE q.id = new.open_question_id);
                regex = (SELECT q.regex FROM questions_open AS q WHERE q.id = new.open_question_id);

                IF (NOT mandatory OR regex IS NULL OR new.text ~ CONCAT('^', regex, '$')) THEN
                    RETURN NEW;
                ELSE
                    RETURN OLD;
                END IF;
            END;
            $$ LANGUAGE plpgsql""")

    connection.execute(
        """DROP TRIGGER IF EXISTS regex_trigger ON answers_open;
        CREATE TRIGGER regex_trigger
        BEFORE INSERT OR UPDATE ON answers_open 
        FOR EACH ROW
        EXECUTE PROCEDURE regex();"""
    )
