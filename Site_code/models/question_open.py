from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, Text
from sqlalchemy.orm import relationship

from context import SQLBase, Session


class OpenQuestion(SQLBase):
    __tablename__ = 'questions_open'

    id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True)
    question = relationship("Question", back_populates="open_question")

    regex = Column(String(200), nullable=True)
    regex_description = Column(String(200), nullable=True)
    mandatory = Column(Boolean, nullable=True)

    open_answers = relationship("OpenAnswer", back_populates="open_question")

