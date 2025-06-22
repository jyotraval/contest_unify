from django.shortcuts import render
from django.db import connections

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json

import chatbot_app.gemini_chatbot as gemini_chatbot


@ensure_csrf_cookie
def show_contests(request):
    with connections['contest_db'].cursor() as cursor:
        cursor.execute("SELECT site, contest_title, event_time, weekday FROM contests ORDER BY unix_time_stamp ASC") 
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        contests = [dict(zip(columns, row)) for row in rows]

        # site_logo_map = {
        # "https://www.hackerearth.com/challenges/": "hackerearth",
        # "https://atcoder.jp/contests/": "atcoder",
        # "https://www.codechef.com/contests": "codechef",
        # "https://leetcode.com/contest/": "leetcode",
        # "https://codeforces.com/contests": "codeforces"
        # }
        # for var in contests:
        #     var['domain'] = site_logo_map.get(var['site'],'NA')
        # # print(contests)

    return render(request, 'contests/index.html', {'contests': contests})


def chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            selected_site = data.get('site','None')

            if not user_message:
                return JsonResponse({'error': 'Empty message'}, status=400)

            # Call Gemini chatbot with the user message and model
            bot_reply = gemini_chatbot.llm_respond(user_message, selected_site)
            # print(bot_reply)

            return JsonResponse({'reply': bot_reply})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return render(request, 'chatbot_index.html')
    

