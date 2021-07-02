from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, Text, event
from sqlalchemy.orm import relationship

from context import SQLBase, Session
from .utils import denyUpdate


class OpenQuestion(SQLBase):
    __tablename__ = 'questions_open'

    id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True)
    question = relationship("Question", back_populates="open_question")

    regex = Column(String(200), nullable=True)
    regex_description = Column(String(200), nullable=True)
    mandatory = Column(Boolean)

    open_answers = relationship("OpenAnswer", back_populates="open_question")

@event.listens_for(OpenQuestion.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    denyUpdate(connection, OpenQuestion.__tablename__)

