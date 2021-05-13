from sqlalchemy.orm import declarative_base

app = None
engine = None
login_manager = None
SQLBase = declarative_base()
Session = None
