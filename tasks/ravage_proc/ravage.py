from tasks.fight_analysis.normalization import Normalization
from utils import catcher, unit, ranking
import os, json

def check_player(players):
    skyfury = False
    source_id = None
    for role in ['tanks', 'healers', 'dps']:
        for player_json in players[role]:
            player = unit.Player(player_json)
            if player.isSpec('Feral'):
                source_id = player.id
            if player.isClass('Shaman'):
                skyfury = True
    return {
        'skyfury': skyfury,
        'source_id': source_id
    }

def ravage_counter(code, fight_id):
    """
    Count the number of Ravage casts in a specific fight.

    Args:
        code (str): The code to identify the player or instance.
        fight_id (int): The ID of the fight to analyze.

    Returns:
        int: The number of Ravage casts.
    """
    players = catcher.player_data(code, fight_id)
    source_info = check_player(players)
    table_data = catcher.table_data(code, fight_ids=fight_id, source_id=source_info['source_id'], data_type='DamageDone')
    with open('data_json/table_data.json', 'w') as f:
        json.dump(table_data, f, indent=4)
    aa_table_data = next((entry for entry in table_data['data']['entries'] if entry.get('guid') == 1), None)
    ravage_table_data = next((entry for entry in table_data['data']['entries'] if entry.get('guid') == 441591), None)
    if aa_table_data is None or ravage_table_data is None:
        raise ValueError("No entry with guid == 1 or spellId == 441591 found in table_data['data']['entries']")
    ravage_casts = ravage_table_data['uses']
    aa_casts = aa_table_data['uses']

    return {
        'skyfury': source_info['skyfury'],
        'ravage_casts': ravage_casts,
        'aa_casts': aa_casts,
        'ravage_proc_index': ravage_casts / aa_casts if aa_casts > 0 else 0,
    }

def fetch_data():
    # zones = ['Darkflame Cleft', 'Cinderbrew Meadaery', 'Operation: Floodgate', 'Operation: Mechagon - Workshop', 'Priory of the Sacred Flame', 'The MOTHERLODE!!', 'The Rookery', 'Theater of Pain']
    top_feral_encounters = ranking.load_top_feral_apex_data(file_path='data_json/top_ferals_20250710_135015.json', top=100)
    result = []
    if top_feral_encounters:
        fights = ranking.fights_parser(top_feral_encounters, extra_info={"key": "normalization", "func": ravage_counter})
        for fight in fights:
            norm = fight.get('ravage_counter')
            result.append({
                'code': fight['report_code'],
                'fight_id': fight['fight'],
                'region': fight['region'],
                'name': fight['name'],
                'fight_name': fight['fight_name'],
                'ravage_counter': norm
            })
        os.makedirs('data_json', exist_ok=True)
        with open(f'data_json/ravage_proc.json', 'w') as f:
            json.dump(result, f, indent=4)

if __name__ == "__main__":
    fetch_data()
