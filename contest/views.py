from django.shortcuts import render
from .connection import get_supabase_connection

def show_supabase_contests(request):
    contests = []
    conn = get_supabase_connection()

    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT site, contest_title, event_time, weekday
                FROM contests
                ORDER BY unix_time_stamp ASC
            """)
            rows = cursor.fetchall()
            for row in rows:
                contests.append({
                    'site': row[0],
                    'title': row[1],
                    'time': row[2],
                    'weekday': row[3]
                })
                # print("Contests from Supabase:", contests)
            cursor.close()
        except Exception as e:
            print("Error fetching from Supabase:", e)
        finally:
            conn.close()

    return render(request, 'index.html', {'contests': contests})
