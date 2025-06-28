# warcraftlogs fetcher
import requests
import json
import argparse
api_key = "b2f77f8c407537b14bb181ce796e1a0a"  # Replace with your API key
def fetch_fights_data(report_code):

    # Define the API endpoint and parameters
    api_url = "https://www.warcraftlogs.com/v1/report/fights/"

    params = {
        'api_key': api_key,
        'translate': 'false'
    }

    # Make the API request
    response = requests.get(f"{api_url}{report_code}", params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def fetch_events_data(view,code,start=0,end=9999999999,ability_id=391882):
    """
    Fetch events data from Warcraft Logs API for a specific report.
    """
    api_url = "https://www.warcraftlogs.com/v1/report/events/"
    params = {
        'api_key': api_key,
        'start': start,  # Start time in milliseconds
        'end': end,  # Adjust as needed
        'abilityid': ability_id,  # Adjust as needed
    }
    response = requests.get(f"{api_url}{view}/{code}", params=params)
    if response.status_code == 200:
        data = response.json()
        with open(f'data_json/{view}_{code}.json', 'w') as f:
            json.dump(data, f, indent=4)
        return data
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


def calculate_feral_apex_procs(fight_data, code):
    """
    Calculate the number of Feral Apex procs from the report data.
    This function assumes that the report data contains relevant events.
    """
    with open(f'data_json/fights_{code}.json', 'w') as f:
        json.dump(fight_data, f, indent=4)
    for fight in fight_data['fights']:
        # Check if the fight has a kill status
        if 'kill' in fight and fight['kill']:
            start = fight['start_time']
            end = fight['end_time']
            print(f"Processing fight {fight['id']} from {start} to {end}")
            rip_ticks = fetch_events_data('damage-done', code, start, end, 1079)
            apex_procs = fetch_events_data('buffs', code, start, end, 391882)
            apex_procs_count = sum(
                1 for apex_event in apex_procs['events']
                if apex_event.get('type') in ('applybuff', 'refreshbuff')
            ) if apex_procs else 0
            rip_ticks_count = len(rip_ticks['events']) if rip_ticks else 0
            apex_index = rip_ticks_count/apex_procs_count if apex_procs_count > 0 else 0
            print(f"Feral Apex procs for fight {fight['id']}: {apex_procs_count}, Rip ticks: {rip_ticks_count}, Apex Index: {apex_index:.2f}")

def main():
    parser = argparse.ArgumentParser(description='Fetch Warcraft Logs data for a specific report.')
    parser.add_argument('report_code', type=str, help='The report code to fetch data for.')
    args = parser.parse_args()
    data = fetch_fights_data(args.report_code)
    
    if data:
        print(f"Fetched data for report {args.report_code}:")
        calculate_feral_apex_procs(data, args.report_code)
    else:
        print("Failed to fetch data.")

if __name__ == "__main__":
    main()