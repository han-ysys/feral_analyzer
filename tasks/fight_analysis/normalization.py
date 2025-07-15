from utils import catcher, unit, ranking
import numpy as np
from sklearn.linear_model import LinearRegression
import argparse
import json
import os
import matplotlib.pyplot as plt
from gooey import Gooey

class Normalization:
    def __init__(self, code, ids, source_id=None):
        self.code = code
        self.ids = ids
        self.skyfury = 0
        players = catcher.player_data(code, ids)
        for role in ['tanks', 'healers', 'dps']:
            for player_json in players[role]:
                player = unit.Player(player_json)
                if player.isSpec('Feral'):
                    self.source_id = player.id
                    self.mastery = player.combatantInfo['stats']['Mastery']
                if player.isClass('Shaman'):
                    self.skyfury = 1
        
    def dmg(self):
        table_data = catcher.table_data(self.code, fight_ids=self.ids, source_id=self.source_id, data_type='DamageDone')
        aa_table_data = next((entry for entry in table_data['data']['entries'] if entry.get('guid') == 1), None)
        if aa_table_data is None:
            raise ValueError("No entry with guid == 1 found in table_data['data']['entries']")
        avg = aa_table_data['total']/aa_table_data['hitCount']
        cast = aa_table_data['uses']
        self.aa_data = { 'avg': avg, 'cast': cast }
        self.overall_dmg = sum(
            entry['total'] for entry in table_data['data']['entries']
            ) if table_data.get('data', {}).get('entries', []) else 0
        self.overall_dps = self.overall_dmg / (table_data['data']['totalTime'] / 1000) if table_data['data']['totalTime'] > 0 else 0

def regression_plot(h,i,j,y, instance, model):
    # 3D scatter plot for the first two features and y
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(h,i,y, c='b', marker='o', label='Actual Data')
    # Regression plane
    h_surf, i_surf = np.meshgrid(
        np.linspace(h.min(), h.max(), 10),
        np.linspace(i.min(), i.max(), 10)
    )
    j_mean = np.mean(j)
    y_surf = (model.intercept_ +
              model.coef_[0] * h_surf +
              model.coef_[1] * i_surf +
              model.coef_[2] * j_mean)
    ax.plot_surface(h_surf, i_surf, y_surf, color='r', alpha=0.5, label='Regression Plane')
    # Plot the instance dot
    ax.scatter(
        instance.aa_data['avg'],
        instance.mastery['min'],
        instance.overall_dps,
        c='g', marker='^', s=100, label='Current Instance'
    )
    ax.set_xlabel('AA Avg')
    ax.set_ylabel('Mastery (min)')
    ax.set_zlabel('Overall DPS')
    plt.title('Regression Diagram (Skyfury fixed at mean)')
    plt.legend()
    plt.show()
        
def normalization_index_regression(normalizations):
    h_array = []
    i_array = []
    j_array = []
    y_array = []
    for instance in normalizations:
        h_array.append(list(instance['aa_data'].values())[0])
        i_array.append(instance['mastery']['min'])
        j_array.append(instance['skyfury'])
        y_array.append(instance['overall_dps'])
    h = np.array(h_array)
    i = np.array(i_array)
    j = np.array(j_array)
    X = np.column_stack((h, i, j))
    y = np.array(y_array)
    model = LinearRegression()
    model.fit(X, y)
    print("Intercept:", model.intercept_)
    print("Coefficient for melee:", model.coef_[0])
    print("Coefficient for mastery:", model.coef_[1])
    print("Coefficient for skyfury:", model.coef_[2])
    return h,i,j,y, model

def check_model(code, fight_id, threshold=100, normalization_file='data_json/normalization.json'):
    instance = Normalization(code, fight_id)
    fight = next((f for f in catcher.fights_data(code)['fights'] if f['id'] == fight_id), None)
    if fight is None:
        raise ValueError(f"No fight found with id={fight_id}")
    fight_name = fight['gameZone']['name']
    if not os.path.exists(normalization_file):
        fetch_normalize_data()
    with open(normalization_file, 'r') as f:
        data = json.load(f)
        normalizations = []
        fight = 0
        for example_fight in data:
            if example_fight['fight_name'] == fight_name:
                normalizations.append(example_fight['normalization'])
                fight += 1
                if fight >= threshold:
                    break
        h,i,j,y, model = normalization_index_regression(normalizations)
    instance.dmg()
    regression_plot(h,i,j,y, instance, model)
    prediction = model.predict(np.array([[instance.aa_data['avg'], instance.mastery['min'], instance.skyfury]]))

    print("Predicted overall dps:", prediction[0])
    print("Actual overall dps:", instance.overall_dps)

def fetch_normalize_data():
    # zones = ['Darkflame Cleft', 'Cinderbrew Meadaery', 'Operation: Floodgate', 'Operation: Mechagon - Workshop', 'Priory of the Sacred Flame', 'The MOTHERLODE!!', 'The Rookery', 'Theater of Pain']
    top_feral_encounters = ranking.load_top_feral_apex_data(file_path='data_json/top_ferals_20250710_135015.json', top=50)
    normalizations = []
    if top_feral_encounters:
        fights = ranking.fights_parser(top_feral_encounters, extra_info={"key": "normalization", "func": Normalization})
        for fight in fights:
            norm = fight.get('normalization')
            normalizations.append({
                'code': fight['report_code'],
                'fight_id': fight['fight'],
                'region': fight['region'],
                'name': fight['name'],
                'fight_name': fight['fight_name'],
                'normalization': {
                    'source_id': norm.source_id,
                    'mastery': norm.mastery,
                    'skyfury': norm.skyfury,
                    'aa_data': norm.aa_data,
                    'overall_dps': norm.overall_dps
                }
            })
        os.makedirs('data_json', exist_ok=True)
        with open(f'data_json/normalization.json', 'w') as f:
            json.dump(normalizations, f, indent=4)

# @Gooey(program_name="Feral DPS Normalizer", default_size=(800, 600))
def main():
    parser = argparse.ArgumentParser(description='Normalization Analysis')
    parser.add_argument('-c', '--code', type=str, required=True, help='Code for the fight')
    parser.add_argument('-f', '--fight_id', type=int, required=True, help='Fight ID for checking the model')
    parser.add_argument('-t', '--top', type=int, default=100, help='Number of top fights to consider for normalization analysis')
    parser.add_argument('-u', '--update', action='store_true', help='Update the normalization data')
    parser.add_argument('-i', '--input', type=str, help='Input file for normalization data(Optional)')
    args = parser.parse_args()
    if args.update:
        fetch_normalize_data()
    check_model(args.code, args.fight_id, threshold=args.top)
    
if __name__ == '__main__':
    main()