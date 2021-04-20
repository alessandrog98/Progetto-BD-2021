import sqlalchemy
from sqlalchemy import *
import urllib
from sqlalchemy import create_engine
import pyodbc as pyodbc

driver = "{ODBC Driver 17 for SQL Server}"
server = "db-project-2021.database.windows.net"
database = "DB project 2021"
user = "Alessandro_878169"
password = "Progetto2021"

conn = f"""Driver={driver};Server=tcp:{server},1433;Database={database};
Uid={user};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"""

params = urllib.parse.quote_plus(conn)
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine = create_engine(conn_str, echo=True)

engine.execute("SELECT 1")
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
