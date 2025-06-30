import json
from tqdm import tqdm

def load_top_feral_apex_data(file_path='data_json/top_ferals.json'):
    """
    Load the top feral apex data from a JSON file.
    
    :param file_path: Path to the JSON file containing top feral apex data.
    :return: Parsed JSON data as a dictionary.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        encounters = data['data']['worldData']['zone']['encounters']
        return encounters
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return {}
    
def fights_parser(encounters, extra_info=None):
    """
    Parse the encounters to extract fights codes and region and encounter names.
    
    :param encounters: List of encounter data.
    :return: Dictionary mapping fight to their details.
    """
    fights = []
    for encounter in encounters:
        fight_name = encounter['name']
        rankings = encounter['characterRankings']['rankings']
        for player in tqdm(rankings, desc=f"Parsing {fight_name}", leave=False):
            fight_code = player['report']['code']
            fight_id = player['report']['fightID']
            region = player['server']['region']
            name = player['name']
            fight_entry = {
            'fight_name': fight_name,
            'report_code': fight_code,
            'region': region,
            'name': name,
            'fight': fight_id
            }
            if extra_info:
                key = extra_info.get('key')
                func = extra_info.get('func')
                if callable(func):
                    value = func(fight_code, fight_id)
                else:
                    value = None
                fight_entry[key] = value
            fights.append(fight_entry)
    return fights