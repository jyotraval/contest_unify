# contest/connection.py

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_supabase_connection():
    try:
        conn = psycopg2.connect(
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            port=os.getenv("port"),
            dbname=os.getenv("dbname")
        )
        print("✅ Supabase connection successful.")
        return conn
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return None
