from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, Text, CheckConstraint, event
from sqlalchemy.orm import relationship

from context import SQLBase, Session
from .utils import denyUpdate


class QuestionTypes(Enum):
    OpenQuestion = 1
    ClosedQuestion = 2


class Question(SQLBase):
    __tablename__ = 'questions'
    __table_args__ = (
        CheckConstraint('LENGTH(title) > 0'),
        CheckConstraint('LENGTH(text) > 0'),
    )

    id = Column(Integer, primary_key=True)
    order = Column(Integer)
    title = Column(String(150))
    text = Column(Text)

    survey_id = Column(Integer, ForeignKey("surveys.id", ondelete="CASCADE"))
    survey = relationship("Survey", back_populates="questions")

    closed_question = relationship("ClosedQuestion", uselist=False, back_populates="question")
    open_question = relationship("OpenQuestion", uselist=False, back_populates="question")

    def get_type(self):
        if self.closed_question is not None and self.open_question is None:
            return QuestionTypes.ClosedQuestion
        elif self.closed_question is None and self.open_question is not None:
            return QuestionTypes.OpenQuestion
        else:
            return None  # TODO Exception


@event.listens_for(Question.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    denyUpdate(connection, Question.__tablename__)
