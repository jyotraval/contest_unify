import os
import psycopg2
from dotenv import load_dotenv
from psycopg2 import OperationalError

# Load environment variables from .env
load_dotenv()

# USER = os.getenv("user")
# PASSWORD = os.getenv("password")
# HOST = os.getenv("host")
# PORT = os.getenv("port")
# DBNAME = os.getenv("dbname")

# connection = psycopg2.connect(
#         user=USER,
#         password=PASSWORD,
#         host=HOST,
#         port=PORT,
#         dbname=DBNAME
#     )


REQUIRED_ENV_VARS = ["user", "password", "host", "port", "dbname"]
env_vars = {var: os.getenv(var) for var in REQUIRED_ENV_VARS}

# print(env_vars)

missing_vars = [key for key, value in env_vars.items() if value is None]
if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

def get_contests_from_supabase():
    try:
        with psycopg2.connect(**env_vars) as conn:
            with conn.cursor() as cursor:
                
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'contests'
                    ORDER BY ordinal_position;
                """)
                # columns = [row[0] for row in cursor.fetchall()]

                # Fetch all data from contests table
                cursor.execute("SELECT site, contest_title, event_time, weekday FROM contests ORDER BY unix_time_stamp;")
                contests = cursor.fetchall()
                # for row in rows:
                #     print(row)
                return contests

        print("Database operations completed successfully.")

    except OperationalError as e:
        print(f"Database connection error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print(get_contests_from_supabase())
    pass

