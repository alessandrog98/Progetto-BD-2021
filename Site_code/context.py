from sqlalchemy.orm import declarative_base


class Context:
    app = None
    engine = None
    login_manager = None
    SQLBase = declarative_base()


context = Context()
