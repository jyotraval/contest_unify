# imprt the requred libbrary
import requests

# fecth leetCode contsts data usng GraphQL API
def fetch_leetcode_contests(url='https://leetcode.com/graphql'):
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
        return response.json()


# Main fucntion to excute the sccript
if __name__=="__main__":
    url='https://leetcode.com/graphql'
    data = fetch_leetcode_contests(url)
    print(data)
