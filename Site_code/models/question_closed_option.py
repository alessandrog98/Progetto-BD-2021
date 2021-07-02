from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, Text, CheckConstraint, event
from sqlalchemy.orm import relationship

from context import SQLBase, Session
from .utils import denyUpdate


class ClosedQuestionOption(SQLBase):
    __tablename__ = 'questions_closed_options'

    id = Column(Integer, primary_key=True)
    order = Column(Integer)
    text = Column(Text)

    closed_question_id = Column(Integer, ForeignKey("questions_closed.id", ondelete="CASCADE"))
    closed_question = relationship("ClosedQuestion", back_populates="closed_question_options")

    closed_answers = relationship("ClosedAnswer", back_populates="closed_question_option")


@event.listens_for(ClosedQuestionOption.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    denyUpdate(connection, ClosedQuestionOption.__tablename__)
