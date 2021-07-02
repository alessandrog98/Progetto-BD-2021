from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, Text, DDL, event
from sqlalchemy.orm import relationship

from context import SQLBase, Session
from .utils import denyUpdate


class ClosedAnswer(SQLBase):
    __tablename__ = 'answers_closed'

    id = Column(Integer, primary_key=True)

    closed_question_option_id = Column(Integer, ForeignKey("questions_closed_options.id", ondelete="CASCADE"))
    closed_question_option = relationship("ClosedQuestionOption", back_populates="closed_answers")

    answer_id = Column(Integer, ForeignKey("answers.id", ondelete="CASCADE"))
    answer = relationship("Answer", back_populates="closed_answers")


@event.listens_for(ClosedAnswer.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    denyUpdate(connection, ClosedAnswer.__tablename__)
