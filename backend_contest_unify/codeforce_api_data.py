import requests

def fetch_api_data(url="https://codeforces.com/api/contest.list",limit=10,target_phase='before'):
    response = requests.get(url) #return response, is it 200,404 etc

    # response.raise_for_status()# Raises error for bad responses (4xx/5xx)

    contests = response.json() #converts into dictionary
    # print(contests.keys()) # $$ status=OK and result=list of contest
    contests = contests.get('result')
    contests= contests[:limit]

    res=[]
    for contest in contests:
        if contest.get("phase", "").lower() == target_phase.lower():
            #only fetch's one is upcomming.
            res.append(contest)
    
    return tuple(res)


if __name__=="__main__":
    # import time
    # strt=time.time()
    url = "https://codeforces.com/api/contest.list"
    print(fetch_api_data(url))


    # print(strt-time.time())
