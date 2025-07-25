import os
import requests

CLIENT_ID = os.getenv("WCL_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("WCL_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
TOKEN_URL = "https://www.warcraftlogs.com/oauth/token"
API_URL = "https://www.warcraftlogs.com/api/v2/client"

def get_access_token():
    data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=data)
    response.raise_for_status()
    return response.json()['access_token']

def send_request(query, variables):
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    # print(f"Sending request to {API_URL} with query: {query} and variables: {variables}")
    for retry in range(10):
        try:
            response = requests.post(API_URL, json={'query': query, 'variables': variables}, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Retrying ({retry + 1}/10)...")
            if retry == 9:
                raise
    return None