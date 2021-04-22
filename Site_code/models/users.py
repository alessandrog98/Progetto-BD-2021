from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float, Date, Table

class User(UserMixin):
    id = Column(Integer,primary_key=True)
    email = Column(String(80))
    name = Column(String(80))
    password = Column(String(80))
    def __init__(self, id, email, pwd):
        self.id = id
        self.email = email
        self.pwd = pwd

    def get_id(self):
        return self.id
