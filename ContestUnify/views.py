from django.shortcuts import render
from django.db import connections

def show_contests(request):
    with connections['contest_db'].cursor() as cursor:
        cursor.execute("SELECT site, contest_title, event_time, weekday FROM contests ORDER BY unix_time_stamp ASC") 
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        contests = [dict(zip(columns, row)) for row in rows]

    return render(request, 'contests/index.html', {'contests': contests})
