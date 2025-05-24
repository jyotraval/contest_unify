import requests
from datetime import datetime, timedelta

def fetch_hackerath_api_contest(url='https://www.hackerearth.com/api/events/upcoming/'):
    response = requests.get(url) 
    response.raise_for_status()

    contests = response.json()
    contests=contests['response']
    
    res=[]
    for i in contests:
        if i["status"].lower()== "UPCOMING".lower():
            date_str=i['start_tz']
            dt_part, tz_part = date_str[:-6], date_str[-6:]

            #date time apart
            dt = datetime.strptime(dt_part, "%Y-%m-%d %H:%M:%S")

            # parse the timezone offset
            sign = 1 if tz_part[0] == '+' else -1
            offset_hours = int(tz_part[1:3])
            offset_minutes = int(tz_part[4:6])
            offset = timedelta(hours=sign * offset_hours, minutes=sign * offset_minutes)

            # normaliez to UTC 0:00
            dt_utc = dt - offset

            # ist offset +0530
            ist_offset = timedelta(hours=5, minutes=30)
            dt_ist = dt_utc + ist_offset

            # time tuple for database feasible CRUD 
            time_tuple= (dt_ist.year, dt_ist.month, dt_ist.day, dt_ist.hour, dt_ist.minute, dt_ist.second, dt_ist.strftime('%A'))

            res.append((i['title'],time_tuple))
    
    return res


if __name__=='__main__':
    print(fetch_hackerath_api_contest())
