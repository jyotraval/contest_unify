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
            site_logo_map = {
        "https://www.hackerearth.com/challenges/": "hackerearth",
        "https://atcoder.jp/contests/": "atcoder",
        "https://www.codechef.com/contests": "codechef",
        "https://leetcode.com/contest/": "leetcode",
        "https://codeforces.com/contests": "codeforces"
    }
            rows = cursor.fetchall()
            for row in rows:
                contests.append({
                    'site': row[0],
                    'title': row[1],
                    'time': row[2][:-6],
                    'weekday': row[3],
                    'domain':site_logo_map.get(row[0],'NA')
                })
                # print("Contests from Supabase:", contests)
                cursor.execute('''
                    SELECT date_trunc('second', human_read AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Kolkata') AS human_read_ist
                    FROM contest_meta_refresh;
                ''')
                lastrefresh = cursor.fetchone()
                if lastrefresh and lastrefresh[0]:
                    lastrefresh = str(lastrefresh[0])
                else:
                    lastrefresh = "N/A"


            cursor.close()
        except Exception as e:
            print("Error fetching from Supabase:", e)
        finally:
            conn.close()

    return render(request, 'index.html', {'contests': contests, 'lastrefresh': lastrefresh})
    # return render(request, 'index.html', {'contests': contests})
