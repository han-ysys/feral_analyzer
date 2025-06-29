import json
import apex_analyzer

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
            apex_index = apex_analyzer.fight_apex_index(fight_code, fight_id)
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

def save_apex_index_summary(file_path='data_json/top_feral_apex_summary.json'):
    top_feral_encounters = load_top_feral_apex_data()
    if top_feral_encounters:
        fights = fights_parser(top_feral_encounters)
        with open(file_path, 'w') as f:
            json.dump(fights, f, indent=4)
        print("Top feral apex summary data saved to 'data_json/top_feral_apex_summary.json'.")
    else:
        print("No data available to process.")

        
if __name__ == "__main__":
    save_apex_index_summary()