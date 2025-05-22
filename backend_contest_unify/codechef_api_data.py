import requests
from datetime import datetime

def fetch_codechef_contests(url='https://www.codechef.com/api/list/contests/all'):
    headers = {'User-Agent':'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    if response.status_code==200:
        data = response.json()
        # print(data)
        contests= data['future_contests']  # upcoming contests
        # print(contests)
    else:
        raise Exception(f"Request failed: {response.status_code}")


    formatted = []

    for contest in contests:
        name = contest['contest_name']
        start_str=contest['contest_start_date']  #'03 jun 2025 20:05:00'
        # Parse str -> obj
        dt=datetime.strptime(start_str, "%d %b %Y %H:%M:%S")

        
        contest_tuple = (
            name,
            (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.strftime("%A"))
        )
        formatted.append(contest_tuple)
    return formatted




if __name__== '__main__':
    
    for contest in  fetch_codechef_contests():
        print(contest)
