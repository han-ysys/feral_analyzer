import json
import os
from utils import catcher

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
    
def frenzy_calculaor(report_code, fight_ids):
    """
    Calculate the total frenzy damage for a given report code and fight ID.
    
    :param report_code: The report code of the fight.
    :param fight_id: The ID of the fight.
    :return: Total frenzy damage.
    """
    events = catcher.events_data(
        report_code=report_code,
        fight_ids=fight_ids,
        ability_id=391140,  # Frenzy ability ID
        event_type='DamageDone'
        )
    total_frenzy_damage = sum(event['amount'] for event in events if 'amount' in event)
    return total_frenzy_damage

def berserk_calculator(report_code, fight_ids):
    """
    Calculate the total berserk damage for a given report code and fight ID.
    
    :param report_code: The report code of the fight.
    :param fight_id: The ID of the fight.
    :return: Total berserk damage.
    """
    events = catcher.events_data(
        report_code=report_code,
        fight_ids=fight_ids,
        ability_id=106951,  # Berserk ability ID
        event_type='Buffs'
        )
    cast_amount = sum(
            1 for event in events
            if event.get('type') in ('applybuff')
        ) if events else 0
    return cast_amount
    
def frenzy_per_berserk(report_code, fight_id):
    accumulated_frenzy_damage = frenzy_calculaor(report_code, fight_id)
    berserk_amount = berserk_calculator(report_code, fight_id)
    if berserk_amount > 0:
        return accumulated_frenzy_damage / berserk_amount
    else:
        return 0.0
    
def frenzy_per_berserk_from_table(report_code, fight_id):
    """
    Calculate frenzy per berserk from a table of fights.
    
    :param report_code: The report code of the fight.
    :param fight_id: The ID of the fight.
    :return: Frenzy per berserk value.
    """
    frenzy = catcher.table_data(
        report_code=report_code,
        fight_ids=fight_id,
        ability_id=391140,  # Frenzy ability ID
        data_type='DamageDone'
        )
    frenzy_sum = sum(
        entry['hitdetails'][0]['total'] for entry in frenzy.get('data', {}).get('entries', [])
    ) if frenzy.get('data', {}).get('entries', []) else 0
    berserk = catcher.table_data(
        report_code=report_code,
        fight_ids=fight_id,
        ability_id=106951,  # Berserk ability ID
        data_type='Buffs'
        )
    auras = berserk.get('data', {}).get('auras', [])
    berserk_amount = sum(
        aura['totalUses'] for aura in auras
    ) if auras else 0
    return frenzy_sum / berserk_amount if berserk_amount > 0 else 0.0

# todo: damage per berserk

if __name__ == "__main__":
    # test
    frenzy_per_berserk_from_table('fLDvVp8YqtkrHmdc', 11)