import requests
import json
import argparse
import os

# Set your client ID and secret here or use environment variables
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

def fetch_events_data(report_code, fight_id, start, end, ability_id, event_type, token):
    query = """
    query ($code: String!, $fightID: Int!, $start: Int!, $end: Int!, $abilityID: Int!, $eventType: DataType!) {
      reportData {
        report(code: $code) {
          events(
            fightIDs: [$fightID]
            startTime: $start
            endTime: $end
            abilityID: $abilityID
            dataType: $eventType
          ) {
            data
          }
        }
      }
    }
    """
    variables = {
        "code": report_code,
        "fightID": fight_id,
        "start": start,
        "end": end,
        "abilityID": ability_id,
        "eventType": event_type
    }
    headers = {"Authorization": f"Bearer {token}"}
    print("Query:", query)
    print("Variables:", variables)
    response = requests.post(API_URL, json={'query': query, 'variables': variables}, headers=headers)
    response.raise_for_status()
    return response.json()['data']['reportData']['report']['events']['data']

def calculate_feral_apex_procs(fight_data, code, token):
    os.makedirs('data_json', exist_ok=True)
    with open(f'data_json/fights_{code}.json', 'w') as f:
        json.dump(fight_data, f, indent=4)
    for fight in fight_data['fights']:
        if fight.get('kill'):
            start = fight['startTime']
            end = fight['endTime']
            fight_id = fight['id']
            print(f"Processing fight {fight_id} from {start} to {end}")
            rip_ticks = fetch_events_data(code, fight_id, start, end, 1079, "DamageDone", token)
            apex_procs = fetch_events_data(code, fight_id, start, end, 391882, "Buffs", token)
            apex_procs_count = sum(
                1 for event in apex_procs
                if event.get('type') in ('applybuff', 'refreshbuff')
            ) if apex_procs else 0
            rip_ticks_count = len(rip_ticks) if rip_ticks else 0
            apex_index = rip_ticks_count / apex_procs_count if apex_procs_count > 0 else 0
            print(f"Feral Apex procs for fight {fight_id}: {apex_procs_count}, Rip ticks: {rip_ticks_count}, Apex Index: {apex_index:.2f}")

def main():
    parser = argparse.ArgumentParser(description='Fetch Warcraft Logs data for a specific report (API v2).')
    parser.add_argument('report_code', type=str, help='The report code to fetch data for.')
    args = parser.parse_args()
    token = get_access_token()
    report = fetch_fights_data(args.report_code, token)
    if report:
        print(f"Fetched data for report {args.report_code}:")
        calculate_feral_apex_procs(report, args.report_code, token)
    else:
        print("Failed to fetch data.")

if __name__ == "__main__":
    main()