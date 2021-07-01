from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, Text, CheckConstraint
from sqlalchemy.orm import relationship

from context import SQLBase, Session


class ClosedQuestion(SQLBase):
    __tablename__ = 'questions_closed'

    id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True)
    question = relationship("Question", back_populates="closed_question")

    min_n_of_answer = Column(Integer)
    max_n_of_answer = Column(Integer)

    closed_question_options = relationship("ClosedQuestionOption", back_populates="closed_question")
    CheckConstraint('(SELECT COUNT(closed_question_options))>=min_n_of_answer OR (SELECT COUNT(closed_question_options))<=max_n_of_answer',
                    name='check_option')
