from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, CheckConstraint, event
from sqlalchemy.orm import relationship

from context import SQLBase, Session
from .utils import denyUpdate


class Survey(SQLBase):
    __tablename__ = 'surveys'
    __table_args__ = (
        CheckConstraint('LENGTH(title) > 0'),
    )

    id = Column(Integer, primary_key=True)
    permit_anon_answer = Column(Boolean)
    title = Column(String(250))

    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    author = relationship("User", back_populates="surveys")

    questions = relationship("Question", back_populates="survey")
    answers = relationship("Answer", back_populates="survey")


@event.listens_for(Survey.__table__, 'after_create')
def receive_after_create(target, connection, **kw):
    denyUpdate(connection, Survey.__tablename__)
