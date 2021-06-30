from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, Text, DDL, event
from sqlalchemy.orm import relationship

from context import SQLBase, Session


class ClosedAnswer(SQLBase):
    __tablename__ = 'answers_closed'

    id = Column(Integer, primary_key=True)

    closed_question_option_id = Column(Integer, ForeignKey("questions_closed_options.id"))
    closed_question_option = relationship("ClosedQuestionOption", back_populates="closed_answers")

    answer_id = Column(Integer, ForeignKey("answers.id"))
    answer = relationship("Answer", back_populates="closed_answers")


maxAns = DDL(
    'CREATE OR REPLACE FUNCTION max_Ans() '
    'RETURNS TRIGGER as $$'
    'DECLARE numAns integer := (SELECT COUNT(*) FROM new.answers_closed);'
    'DECLARE idQ integer := (SELECT closed_question_option_id FROM new.answers_closed LIMIT 1);'
    'BEGIN'
    '   IF (numAns<=(SELECT q.max_n_of_answer '
    '                FROM questions_closed AS q JOIN questions_closed_option AS qc ON q.id=qc.closed_question_id'
    '                WHERE qc.id = idQ LIMIT 1)'
    '       OR numAns>=(SELECT q.min_n_of_answer'
    '                   FROM questions_closed AS q JOIN questions_closed_option AS qc ON q.id=qc.closed_question_id'
    '                   WHERE qc.id = idQ LIMIT 1)) THEN'
    '           RETURN NULL;'
    '   END IF;'
    '   RETURN NEW;'
    'END;'
    '$$ LANGUAGE plpgsql'
)

trigger_maxAns = DDL(
    'DROP TRIGGER IF EXISTS MaxClosedAns ON answers_closed;'
    'CREATE TRIGGER MaxClosedAns'
    'BEFORE INSERT OR UPDATE ON answers_closed '
    'FOR EACH STATEMENT '
    'EXECUTE PROCEDURE max_Ans();'
)

event.listen(ClosedAnswer, 'before_insert', trigger_maxAns)