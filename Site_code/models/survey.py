from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table
from sqlalchemy.orm import relationship

from Site_code.context import SQLBase, Session


class Survey(SQLBase):
    __tablename__ = 'surveys'

    id = Column(Integer, primary_key=True)
    permit_anon_answer = Column(Boolean)
    title = Column(String(150))

    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="surveys")

    questions = relationship("Question", back_populates="survey")
    answers = relationship("Answer", back_populates="survey")
