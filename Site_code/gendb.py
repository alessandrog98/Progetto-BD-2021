import sqlalchemy
from sqlalchemy import *

engine = create_engine('sqlite://', echo=True)
metadata = MetaData()

users = Table('users', metadata, Column('id', Integer, primary_key=True),
                                 Column('email', String),
                                 Column('pwd', String))

addresses = Table('addresses', metadata, Column('id', Integer, primary_key=True),
                                         Column('user_id', None, ForeignKey('users.id')),
                                         Column('email_address', String, nullable=False))

metadata.create_all(engine)

ins = users.insert()
conn = engine.connect()
select_users = users.select()

ins.values(name='jack', pwd='Jack Jones')
conn.execute(ins, name='sally', pwd='Sally Roberts')

for row in conn.execute(select_users):
    print(row)

for row in conn.execute(select([users, addresses])):
    print(row)


print(str(ins))
