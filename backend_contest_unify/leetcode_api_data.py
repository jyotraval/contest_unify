# imprt the requred libbrary
import requests
from time import time

# fecth leetCode contsts data usng GraphQL API
def fetch_leetcode_contests(url='https://leetcode.com/graphql',limit=10):
    headers={
        'Content-Type': 'application/json',
        'Referer': 'https://leetcode.com/contest/',
        'User-Agent': 'Mozilla/5.0'
    }
    
    # GraphQL querry to get contsts infomation
    query={
        "query": """
        {
          allContests {
            title
            titleSlug
            startTime
            duration
          }
        }
        """
    }

    # Make POST requst to the API
    response=requests.post(url, json=query, headers=headers)
    if response.status_code == 200:
        # return response.json()
        data=response.json()
        contests = data['data']['allContests']
        return classify_contests(contests,limit)



def classify_contests(contests,limit=10):
    current_time=int(time())
    classified=[]
    for contest in contests:
        start=contest['startTime']
        duration=contest['duration']
        end=start+duration
        # Check if contest is upcoming/finished
        #if curretnt time is less than start time then its finished
        #if not then its upcming
        if current_time<start:
            status='Upcoming'
        else:
            status = 'Done'
        if status=='Upcoming':
            classified.append({
                'title': contest['title'],
                'startTime': start,
                'duration': duration,
                'status': status
            })
        else:
            break
    return classified


# Main fucntion to excute the sccript
if __name__=="__main__":
    url='https://leetcode.com/graphql'
    # data = fetch_leetcode_contests(url)
    # print(data)
    res = fetch_leetcode_contests(url)
    # print(data)
    # contests = data['data']['allContests']
    # print (contests)
    # import time
    # st=time.time()
    # contests_status = classify_contests(contests,10)
    # print(contests_status,time.time()-st)
    for c in res:
        if c['status'].lower()=='upcoming':
            print(f"{c['title']} - status:{c['status']}-",c)
        else:
            break
