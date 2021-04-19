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

ins = users.insert()
conn = engine.connect()
select_users = users.select()

conn.execute(ins, email='sally@gmail.com', pwd='Sally Roberts')
conn.execute(ins, email='jack@gmail.com', pwd='Jack Jones')
conn.execute(ins, email='prova', pwd='prova')

for row in conn.execute(select_users):
    print(row)

print(str(ins))
