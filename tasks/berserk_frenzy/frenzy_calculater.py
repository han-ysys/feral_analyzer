import json
import os

home_dir = os.getenv("CURRENT_DIR", os.path.expanduser("~"))

def load_top_feral_apex_data(file_path=f'{home_dir}/data_json/top_ferals.json'):
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
    
def frenzy_calculaor(report_code, fight_id):
    """
    Calculate the total frenzy damage for a given report code and fight ID.
    
    :param report_code: The report code of the fight.
    :param fight_id: The ID of the fight.
    :return: Total frenzy damage.
    """
    # Placeholder for actual calculation logic
    # This should interact with an API or database to fetch the data
    # For now, we return a dummy value
    return 1000.0  # Example value, replace with actual calculation logic

def berserk_calculator(report_code, fight_id):
    """
    Calculate the total berserk damage for a given report code and fight ID.
    
    :param report_code: The report code of the fight.
    :param fight_id: The ID of the fight.
    :return: Total berserk damage.
    """
    # Placeholder for actual calculation logic
    # This should interact with an API or database to fetch the data
    # For now, we return a dummy value
    return 5  # Example value, replace with actual calculation logic
    
def frenzy_per_berserk(report_code, fight_id):
    accumulated_frenzy_damage = frenzy_calculaor(report_code, fight_id)
    berserk_amount = berserk_calculator(report_code, fight_id)
    if berserk_amount > 0:
        return accumulated_frenzy_damage / berserk_amount
    else:
        return 0.0
    
def fights_parser(encounters):
    """
    Parse the encounters to extract fights codes and region and encounter names.
    
    :param encounters: List of encounter data.
    :return: Dictionary mapping fight to their details.
    """
    fights = []
    for encounter in encounters:
        fight_name = encounter['name']
        for player in encounter['characterRankings']['rankings']:
            fight_code = player['report']['code']
            fight_id = player['report']['fightID']
            region = player['server']['region']
            name = player['name']
            apex_index = frenzy_per_berserk(fight_code, fight_id)
            fights.append({
                'fight_name': fight_name,
                'report_code': fight_code,
                'region': region,
                'name': name,
                'apex_index': apex_index,
                'fight': fight_id
            })
            print(f"Processed fight: {fight_name}, Code: {fight_code}, Fight ID: {fight_id}, Region: {region}, Name: {name}, Apex Index: {apex_index:.2f}")
    return fights