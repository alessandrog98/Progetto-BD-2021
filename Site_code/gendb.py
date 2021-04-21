import sqlalchemy
from sqlalchemy import *
import urllib
from sqlalchemy import create_engine
import pyodbc as pyodbc
import datetime
from sqlalchemy import Column, Integer, DateTime

driver = "{ODBC Driver 17 for SQL Server}"
server = "questionario.database.windows.net"
database = "questionario"
user = "Kowalskik"
password = "Lego2233"

conn = f"""Driver={driver};Server=tcp:{server},1433;Database={database};
Uid={user};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"""

params = urllib.parse.quote_plus(conn)
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine = create_engine(conn_str, echo=True)

engine.execute("SELECT 1")
metadata = MetaData()

users = Table('Users', metadata, Column('id', Integer, primary_key=True),
                                 Column('email', String),
                                 Column('pwd', String),
                                 Column('IDGruppo', Integer),
                                 )



addresses = Table('Addresses', metadata, Column('id', Integer, primary_key=True),
                                         Column('user_id', None, ForeignKey('Users.id')),
                                         Column('email_address', String, nullable=False)
                                         )

permission= Table('Permissions',metadata,
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
sessions= Table('Sessions',metadata,
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

