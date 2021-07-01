from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table, DDL, event
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from context import SQLBase, login_manager, Session
from models.survey import Survey


class User(UserMixin, SQLBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(80))
    name = Column(String(80))
    password = Column(String(100))

    surveys = relationship("Survey", back_populates="author")
    answers = relationship("Answer", back_populates="user")

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)

    def get_full_name(self):
        return self.name.capitalize()

    @staticmethod
    def get_by_email(email):
        return Session().query(User).filter_by(email=email).first()

    @staticmethod
    @login_manager.user_loader
    def load_user(id):
        return Session().query(User).filter_by(id=int(id)).first()

    def my_surveys(id):
        query = Session().query(Survey).filter_by(author_id=int(id)).all()
        return query
