from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table
from sqlalchemy.orm import relationship

from context import SQLBase, Session

class AnswerTypes(Enum):
    OpenAnswer = 1
    ClosedAnswer = 2

class Answer(SQLBase):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="answers")

    survey_id = Column(Integer, ForeignKey("surveys.id"))
    survey = relationship("Survey", back_populates="answers")

    closed_answers = relationship("ClosedAnswer", back_populates="answer")
    open_answers = relationship("OpenAnswer", back_populates="answer")

    def get_type(self):
        if self.closed_answer is not None and self.open_answer is None:
            return AnswerTypes.ClosedAnswer
        elif self.closed_answer is None and self.open_answer is not None:
            return AnswerTypes.OpenAnswer
        else:
            return None  # TODO ExceptionAns