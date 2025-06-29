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

def fetch_fights_data(report_code, token):
    query = """
    query ($code: String!) {
      reportData {
        report(code: $code) {
          fights {
            id
            startTime
            endTime
            kill
          }
        }
      }
    }
    """
    variables = {"code": report_code}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(API_URL, json={'query': query, 'variables': variables}, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data['data']['reportData']['report']