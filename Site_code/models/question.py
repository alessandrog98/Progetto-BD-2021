from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, Text
from sqlalchemy.orm import relationship

from context import SQLBase, Session


class Question(SQLBase):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    order = Column(Integer)
    title = Column(String(150))
    text = Column(Text)

    survey_id = Column(Integer, ForeignKey("surveys.id"))
    survey = relationship("Survey", back_populates="questions")

    closed_question = relationship("ClosedQuestion", uselist=False, back_populates="question")
    open_question = relationship("OpenQuestion", uselist=False, back_populates="question")
