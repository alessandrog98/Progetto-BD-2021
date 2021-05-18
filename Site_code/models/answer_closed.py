from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, Text
from sqlalchemy.orm import relationship

from context import SQLBase, Session


class ClosedAnswer(SQLBase):
    __tablename__ = 'answers_closed'

    id = Column(Integer, primary_key=True)

    closed_question_option_id = Column(Integer, ForeignKey("questions_closed_options.id"))
    closed_question_option = relationship("ClosedQuestionOption", back_populates="closed_answers")

    answer_id = Column(Integer, ForeignKey("answers.id"))
    answer = relationship("Answer", back_populates="closed_answers")
