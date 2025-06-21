import requests
import json

BASE_URL = "https://codeforces.com/api"

def fetch_api(endpoint):
    try:
        response =requests.get(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        data=response.json()
        
        if data.get("status") != "OK":
            return None
        
        return data
    
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_codeforces_user_data(username):
    user_info=fetch_api(f"user.info?handles={username}")

    if not user_info:
        return {"error": "User not found"}

    user_rating = fetch_api(f"user.rating?handle={username}")
    user_status = fetch_api(f"user.status?handle={username}")
    return {
        "user_info": user_info,
        "user_rating": user_rating,
        "user_status": user_status
    }

if __name__ == '__main__':
    username = 'jyotraval'
    data = get_codeforces_user_data(username)
    print(data['user_info']['result'][0]['rating'])
