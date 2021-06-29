from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, CheckConstraint
from sqlalchemy.orm import relationship

from context import SQLBase, Session


class Survey(SQLBase):
    __tablename__ = 'surveys'

    id = Column(Integer, primary_key=True)
    permit_anon_answer = Column(Boolean)
    title = Column(String(250))

    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="surveys")

    questions = relationship("Question", back_populates="survey")
    answers = relationship("Answer", back_populates="survey")
    CheckConstraint('(SELECT COUNT(quesitons))>=(SELECT COUNT(answers))',name='check_option')