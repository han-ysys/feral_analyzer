from utils import catcher, unit, ranking
import os, json
import numpy as np
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt

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
    # berserk_count = len(list(filter(lambda x: x['type'] == 'applybuff', catcher.events_data(report_code=code, fight_ids=fight_id, source_id=source_info['source_id'], event_type='Buffs', ability_id=106951))))
    with open('data_json/table_data.json', 'w') as f:
        json.dump(table_data, f, indent=4)
    aa_data = aa_details(code, fight_id, source_id=source_info['source_id'])
    ravage_data = ravage_filter(code, fight_id, aa_data['raw'])
    # ravage_table_data = next((entry for entry in table_data['data']['entries'] if entry.get('guid') == 441591), None)
    if aa_data is None or ravage_data is None:
        raise ValueError("No entry with guid == 1 or spellId == 441591 found in table_data['data']['entries']")
    ravage_casts = len(ravage_data)

    return {
        'skyfury': source_info['skyfury'],
        'ravage_casts': ravage_casts,
        'aa_data': aa_data['details'],
        'ravage_proc_index': ravage_casts / aa_data['details']['clean_aa'] if aa_data['details']['clean_aa'] > 0 else 0,
    }

def fetch_data(input_path='data_json/top_ferals_20250710_135015.json', output_path='data_json/ravage_proc_100.json', top=100):
    # zones = ['Darkflame Cleft', 'Cinderbrew Meadaery', 'Operation: Floodgate', 'Operation: Mechagon - Workshop', 'Priory of the Sacred Flame', 'The MOTHERLODE!!', 'The Rookery', 'Theater of Pain']
    top_feral_encounters = ranking.load_top_feral_apex_data(file_path=input_path, top=top)
    result = []
    if top_feral_encounters:
        fights = ranking.fights_parser(top_feral_encounters, extra_info={"key": "ravage_counter", "func": ravage_counter})
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
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=4)

def proc_analysis(file='data_json/ravage_proc.json'):
    with open(file, 'r') as f:
        data = json.load(f)
    ravage_procs = []
    ravage_count = []
    aa_count = []
    skyfury = []
    for entry in data:
        ravage_procs.append(entry['ravage_counter']['ravage_proc_index'])
        ravage_count.append(entry['ravage_counter']['ravage_casts'])
        aa_count.append(entry['ravage_counter']['aa_data']['clean_aa'])
        skyfury.append(entry['ravage_counter']['skyfury'])

    # Analyze if skyfury contributes significantly to ravage_procs
    ravage_procs_skyfury = [proc for proc, sf in zip(ravage_procs, skyfury) if sf]
    print(f"Ravage Procs with Skyfury: {len(ravage_procs_skyfury)}")
    ravage_procs_no_skyfury = [proc for proc, sf in zip(ravage_procs, skyfury) if not sf]
    print(f"Ravage Procs without Skyfury: {len(ravage_procs_no_skyfury)}")

    mean_skyfury = np.mean(ravage_procs_skyfury) if ravage_procs_skyfury else 0
    mean_no_skyfury = np.mean(ravage_procs_no_skyfury) if ravage_procs_no_skyfury else 0

    print(f"Mean Ravage Proc Index with Skyfury: {mean_skyfury:.4f}")
    print(f"Mean Ravage Proc Index without Skyfury: {mean_no_skyfury:.4f}")

    # Optional: simple statistical test (t-test)
    if ravage_procs_skyfury and ravage_procs_no_skyfury:
        t_stat, p_value = ttest_ind(ravage_procs_skyfury, ravage_procs_no_skyfury, equal_var=False)
        print(f"T-test p-value: {p_value:.4f} (p < 0.05 suggests significant difference)")
    # Bar plot with error bars and significance annotation
    means = [mean_skyfury, mean_no_skyfury]
    stds = [
        np.std(ravage_procs_skyfury) if ravage_procs_skyfury else 0,
        np.std(ravage_procs_no_skyfury) if ravage_procs_no_skyfury else 0
    ]
    labels = ['Skyfury', 'No Skyfury']

    fig, ax = plt.subplots()
    bars = ax.bar(labels, means, yerr=stds, capsize=8, color=['skyblue', 'lightgray'], edgecolor='black')

    # Significance annotation
    if ravage_procs_skyfury and ravage_procs_no_skyfury and p_value < 0.05:
        max_height = max(means) + max(stds)
        ax.plot([0, 1], [max_height + 0.01, max_height + 0.01], color='black')
        ax.text(0.5, max_height + 0.015, '*', ha='center', va='bottom', fontsize=20)

    ax.set_ylabel('Ravage Proc Index')
    ax.set_title('Ravage Proc Index by Skyfury Presence')
    plt.tight_layout()
    plt.show()
    
def aa_details(code, fight_id, source_id=None):
    """
    Fetch the AA data for a specific fight and player.

    Args:
        code (str): The code to identify the player or instance.
        fight_id (int): The ID of the fight to analyze.
        source_id (str, optional): The ID of the player. If None, it will be determined from player data.

    Returns:
        dict: The AA data for the specified fight and player.
    """
    if source_id is None:
        players = catcher.player_data(code, fight_id)
        source_info = check_player(players)
        source_id = source_info['source_id']
    
    data = catcher.events_data(report_code=code, fight_ids=[fight_id], source_id=source_id, event_type='DamageDone', ability_id=1)
    # Compare each AA event against its adjacent events
    data = list(data)  # Ensure it's a list for indexing
    double_attack = 0
    total_aa = len(data)
    for i, aa in enumerate(data):
        if i > 0 and i < total_aa - 1:
            prev_aa = data[i - 1]
            if aa['timestamp'] - prev_aa['timestamp'] < 150:
                double_attack += 1
    return {
        'raw': data,
        'details': {
            'double_attack': double_attack,
            'total_aa': total_aa,
            'double_attack_rate': double_attack / total_aa if total_aa > 0 else 0,
            'clean_aa': total_aa - double_attack,
        }
    }

        
def ravage_filter(code, fight_id, aa_data, source_id=None):
    if source_id is None:
        players = catcher.player_data(code, fight_id)
        source_info = check_player(players)
        source_id = source_info['source_id']
    data = catcher.events_data(report_code=code, fight_ids=[fight_id], source_id=source_id, event_type='Buffs', ability_id=441585)
    applies = list(filter(lambda x: x['type'] == 'applybuff', data))
    aa_induced_ravage = []
    for apply in applies:
        if any(True for aa in aa_data if apply['timestamp'] - aa['timestamp'] < 30):
            aa_induced_ravage.append(apply)
    # print(f"Ravage procs induced by AA: {len(aa_induced_ravage)}")
    # print(f"Total Ravage: {len(applies)}")
    return aa_induced_ravage

def test_ravage(code, fight_id, source_id=None):
    """
    Test the ravage counter function with a specific code and fight ID.
    
    :param code: The code to identify the player or instance.
    :param fight_id: The ID of the fight to analyze.
    :return: The result of the ravage counter function.
    """
    # data = catcher.table_data(code, fight_ids=fight_id, source_id=source_id, data_type='DamageDone')
    data = catcher.events_data(report_code=code, fight_ids=[fight_id], source_id=source_id, event_type='DamageDone', ability_id=1)
    print(len(list(data)))
    with open('data_json/aa_data.json', 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    if not os.path.exists('data_json/ravage_proc_100.json'):
        fetch_data(input_path='data_json/top_ferals_20250710_135015.json',output_path='data_json/ravage_proc_100.json',top=100)
    proc_analysis(file='data_json/ravage_proc_100.json')