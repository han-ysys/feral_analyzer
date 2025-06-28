import requests
import json
import argparse
import os

import api

def fetch_events_data(report_code, fight_id, start, end, ability_id, event_type, token):
    query = """
    query ($code: String!, $start: Float, $end: Float, $abilityID: Float, $dataType: EventDataType) {
      reportData {
        report(code: $code) {
          events(startTime: $start, endTime: $end, abilityID: $abilityID, dataType: $dataType) {
            data,
            nextPageTimestamp
          }
        }
      }
    }
    """
    variables = {
        "code": report_code,
        "start": start,
        "end": end,
        "abilityID": ability_id,
        "dataType": event_type
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(api.API_URL, json={'query': query, 'variables': variables}, headers=headers)
    response.raise_for_status()
    data = response.json()['data']['reportData']['report']['events']
    nextPageTimestamp = data.get('nextPageTimestamp')
    if nextPageTimestamp is not None:
        nextPage_data = fetch_events_data(report_code, fight_id, nextPageTimestamp, end, ability_id, event_type, token)
        data['data'].extend(nextPage_data)
    return data['data']

def calculate_feral_apex_procs(fight_data, code, token, fight_id=None):
    # with open(f'data_json/fights_{code}.json', 'w') as f:
    #     json.dump(fight_data, f, indent=4)
    if fight_id is None: # if no specific fight is provided, return first killed fight's Apex Index
        # todo: handle multiple fights
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
                apex_index = apex_procs_count / rip_ticks_count * 100 if rip_ticks_count > 0 else 0
                # print(f"Feral Apex procs for fight {fight_id}: {apex_procs_count}, Rip ticks: {rip_ticks_count}, Apex Index: {apex_index:.2f} %")
        return apex_index
    else:
        # if a specific fight is provided, calculate Apex Index for that fight
        fight_data = next((fight for fight in fight_data['fights'] if fight['id'] == fight_id), None)
        if not fight_data:
            print(f"Fight with ID {fight_id} not found in report {code}.")
            return None
        start = fight_data['startTime']
        end = fight_data['endTime']
        print(f"Processing fight {fight_id} from {start} to {end}")
        rip_ticks = fetch_events_data(code, fight_id, start, end, 1079, "DamageDone", token)
        apex_procs = fetch_events_data(code, fight_id, start, end, 391882, "Buffs", token)
        apex_procs_count = sum(
            1 for event in apex_procs
            if event.get('type') in ('applybuff', 'refreshbuff')
        ) if apex_procs else 0
        rip_ticks_count = len(rip_ticks) if rip_ticks else 0
        apex_index = apex_procs_count / rip_ticks_count * 100 if rip_ticks_count > 0 else 0
        # print(f"Feral Apex procs for fight {fight_id}: {apex_procs_count}, Rip ticks: {rip_ticks_count}, Apex Index: {apex_index:.2f} %")
        return apex_index

def fight_apex_index(code, fight_id=None):
    token = api.get_access_token()
    report = api.fetch_fights_data(code, token)
    if report:
        print(f"Fetched data for report {code}:")
        return calculate_feral_apex_procs(report, code, token, fight_id)
    else:
        print("Failed to fetch data.")

def main():
    parser = argparse.ArgumentParser(description='Fetch Warcraft Logs data for a specific report (API v2).')
    parser.add_argument('report_code', type=str, help='The report code to fetch data for.')
    args = parser.parse_args()
    token = api.get_access_token()
    report = api.fetch_fights_data(args.report_code, token)
    if report:
        print(f"Fetched data for report {args.report_code}:")
        calculate_feral_apex_procs(report, args.report_code, token)
    else:
        print("Failed to fetch data.")

if __name__ == "__main__":
    main()