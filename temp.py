import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("Connection successful!")
    
    cursor = connection.cursor()
    
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Current Time:", result)


    cursor.execute("SELECT * FROM contests;")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    connection.close()

    cursor.close()
    connection.close()
    print("connedtion closed.")

except Exception as e:
    print(f"Failed to connect: {e}")