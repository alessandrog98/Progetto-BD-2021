import urllib
from sqlalchemy import create_engine
from dotenv import dotenv_values

config = dotenv_values("old.env")

driver = "{ODBC Driver 17 for SQL Server}"

conn = f"""Driver={driver};Server=tcp:{config['DB_ADDRESS']},{config['DB_PORT']};Database={config['DB_NAME']};Uid={config['DB_USER']};Pwd={config['DB_PASSWORD']};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"""
params = urllib.parse.quote_plus(conn)
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)


engine = create_engine(conn_str, echo=True)
