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
