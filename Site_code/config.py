import urllib
from sqlalchemy import create_engine

driver = "{ODBC Driver 17 for SQL Server}"
server = "questionario.database.windows.net"
database = "questionario"
user = "Kowalskik"
password = "Lego2233"

conn = f"""Driver={driver};Server=tcp:{server},1433;Database={database};Uid={user};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"""
params = urllib.parse.quote_plus(conn)
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)


engine = create_engine(conn_str, echo=True)
