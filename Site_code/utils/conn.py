import flask
import sqlalchemy
from sqlalchemy import *
from sqlalchemy import create_engine
from gendb import users
from config import conn_str,engine


def Userquery(user_id):
            conn = engine.connect()
            rs = conn.execute(select(users).where(users.c.id == user_id))
            ris = rs.fetchone()
            conn.close()
            return ris
