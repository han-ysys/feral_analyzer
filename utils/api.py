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