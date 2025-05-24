import requests
from datetime import datetime
from zoneinfo import ZoneInfo

def fetch_codeforce_api_data(url="https://codeforces.com/api/contest.list",limit=10,target_phase='before'):
    response = requests.get(url) #return response, is it 200,404 etc

    # response.raise_for_status()# Raises error for bad responses (4xx/5xx)

    contests = response.json() #converts into dictionary
    # print(contests.keys()) # $$ status=OK and result=list of contest
    contests = contests.get('result')
    contests= contests[:limit]

    res=[]
    for contest in contests:
        if contest.get("phase", "").lower() == target_phase.lower():
            start_time = contest.get("startTimeSeconds")
            if start_time:
                # Convert to IST (Asia/Kolkata)
                dt = datetime.fromtimestamp(start_time, ZoneInfo("Asia/Kolkata"))
                time_tuple = (
                    dt.year,
                    dt.month,
                    dt.day,
                    dt.hour,
                    dt.minute,
                    dt.second,
                    dt.strftime('%A')  # Weekday name
                )
                res.append((contest.get("name", "Unknown Title"), time_tuple))


            if len(res) >= limit:
                break
    
    return tuple(res)


if __name__=="__main__":
    # import time
    # strt=time.time()
    url = "https://codeforces.com/api/contest.list"
    url = "https://codeforces.com/api/contest.list"
    for i in fetch_codeforce_api_data(url,10):
        print(i)


    # print(strt-time.time())
