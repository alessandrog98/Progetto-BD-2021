import sqlalchemy
from sqlalchemy import *

engine = create_engine('sqlite:///database.db', echo=True)
metadata = MetaData()

users = Table('Users', metadata, Column('id', Integer, primary_key=True),
                                 Column('email', String),
                                 Column('pwd', String))

addresses = Table('addresses', metadata, Column('id', Integer, primary_key=True),
                                         Column('user_id', None, ForeignKey('Users.id')),
                                         Column('email_address', String, nullable=False))

metadata.create_all(engine)
conn = engine.connect()

ins = users.insert()
sel = users.select()

conn.execute(ins, email='prova', pwd='prova')

for row in conn.execute(sel):
    print(row)

print(str(ins))
