import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

def fetch_atcoder_contests():
    url='https://atcoder.jp/contests/'
    response=requests.get(url)
    if response.status_code!=200:
        raise Exception(f"Failed to fetch contests page: {response.status_code}")

    soup =BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    upcoming_header = soup.find('h3', string='Upcoming Contests')
    
    if not upcoming_header:
        raise Exception("Could not find the 'Upcoming Contests' section.")

    table=upcoming_header.find_next_sibling('div').find('table')
    # print(table)
    contests=[]

    for row in table.find_all('tr')[1:]:  # skip header..get all upcoming contests
        cols=row.find_all('td')
        # print(cols)
        if len(cols)<2:
            continue

        time_str =cols[0].text.strip()  # YYYY-MM-DD HH:MM:SS+0900
        name= cols[1].text.strip()
        # print(name[4:],time_str)
        name=name[4:]

        # AtCoder uses JST japan (UTC+9), so parseing accordingly
        jst =pytz.timezone('Asia/Tokyo')
        ist =pytz.timezone('Asia/Kolkata')
        start_time_jst =datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S%z')
        start_time_ist =start_time_jst.astimezone(ist)
        # print(start_time_jst,start_time_ist)

        dt_tuple = (
            start_time_ist.year,
            start_time_ist.month,
            start_time_ist.day,
            start_time_ist.hour,
            start_time_ist.minute,
            start_time_ist.second,
            start_time_ist.strftime('%A')
        )


        contests.append((name, dt_tuple))

    return contests



if __name__ == "__main__":
    # import time
    # st=time.time()
    contests = fetch_atcoder_contests()
    for i in contests:
        print(-)
    # print(time.time()-st)
