from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, Text
from sqlalchemy.orm import relationship

from context import SQLBase, Session


class ClosedQuestionOption(SQLBase):
    __tablename__ = 'questions_closed_options'

    id = Column(Integer, primary_key=True)
    order = Column(Integer)
    text = Column(Text)

    closed_question_id = Column(Integer, ForeignKey("questions_closed.id"))
    closed_question = relationship("ClosedQuestion", back_populates="closed_question_options")

    closed_answers = relationship("ClosedAnswer", back_populates="closed_question_option")
