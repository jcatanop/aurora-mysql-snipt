import os

import boto3
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ.get("DB_PORT", 3306))
DB_NAME = os.environ.get("DB_NAME", "mysql")
DB_USER = os.environ["DB_USER"]
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
SSL_CA = os.environ.get("SSL_CA", "./global-bundle.pem")

rds_client = boto3.client("rds", region_name=AWS_REGION)
auth_token = rds_client.generate_db_auth_token(
    DBHostname=DB_HOST,
    Port=DB_PORT,
    DBUsername=DB_USER,
)

conn = None
try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=auth_token,
        ssl_disabled=False,
        ssl_ca=SSL_CA,
        auth_plugin='mysql_clear_password',
        autocommit=True,
    )
    cur = conn.cursor()
    cur.execute('SELECT VERSION();')
    print(cur.fetchone()[0])
    cur.close()
except Exception as e:
    print(f"Database error: {e}")
    raise
finally:
    if conn:
        conn.close()
