from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, Text
from sqlalchemy.orm import relationship

from context import SQLBase, Session


class OpenAnswer(SQLBase):
    __tablename__ = 'answers_open'

    id = Column(Integer, primary_key=True)
    text = Column(Text)

    open_question_id = Column(Integer, ForeignKey("questions_open.id"))
    open_question = relationship("OpenQuestion", back_populates="open_answers")

    answer_id = Column(Integer, ForeignKey("answers.id"))
    answer = relationship("Answer", back_populates="open_answers")
