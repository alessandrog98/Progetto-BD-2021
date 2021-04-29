import sqlalchemy
from sqlalchemy import *
import urllib
from sqlalchemy import create_engine
import pyodbc as pyodbc
import datetime
from sqlalchemy import Column, Integer, DateTime



def generaDB(app) :
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    engine.execute("SELECT 1")
    metadata = MetaData()

    users = Table('Users', metadata, Column('id', Integer, primary_key=True),
                                     Column('email', String),
                                     Column('pwd', String),
                                     Column('IDGruppo', Integer),
                                     )



    addresses = Table('addresses', metadata, Column('id', Integer, primary_key=True),
                                             Column('user_id', None, ForeignKey('Users.id')),
                                             Column('email_address', String, nullable=False)
                                             )

    permission= Table('permissions',metadata,
                                    Column('id', Integer, primary_key=True),
                                     Column('IDGruppo', Integer),
                                     Column('Tabella', String),
                                     Column('C', Integer),
                                     Column('R', Integer),
                                     Column('U', Integer),
                                     Column('D', Integer),
                                     Column('Condizione', String),
                                     Column('DataCreazione', TIMESTAMP(timezone=False), nullable=False, default=datetime.datetime.utcnow)
    )
    sessions= Table('sessions',metadata,
                        Column('ID', Integer, primary_key=True),
                         Column('Token', String),
                         Column('IDUser', Integer),
                         Column('IDGruppo', Integer),
                         Column('DataCreazione', TIMESTAMP(timezone=False), nullable=False, default=datetime.datetime.utcnow)
                  )

    metadata.create_all(engine)
    conn = engine.connect()

    ins = users.insert()
    sel = users.select()

    conn.execute(ins, email='prova', pwd='prova')

    for row in conn.execute(sel):
        print(row)

    print(str(ins))
