from utils import catcher, unit
import numpy as np
from sklearn.linear_model import LinearRegression

class Normalization:
    def __init__(self, code, ids, source_id=None):
        self.code = code
        self.ids = ids
        if not source_id:
            players = catcher.player_data(code, ids)
            for player_json in players['dps']:
                player = unit.Player(player_json)
                if player.isSpec('Feral'):
                    self.source_id = player['id']
                    self.mastery = player['combatantInfo']['stats']['Mastery']
                self.skyfury = 1 if player.isSpec('Shaman') else 0
        
    def dmg(self):
        table_data = catcher.table_data(self.code, fight_ids=self.ids, source_id=self.source_id, data_type='DamageDone')
        aa_table_data = filter(lambda x: x['guid'] == 1, table_data['data']['entries'])
        avg = aa_table_data['total']/aa_table_data['hitCount']
        cast = aa_table_data['uses']
        self.aa_data = { avg: avg, cast: cast }
        self.overall_dmg = sum(
            entry['total'] for entry in table_data['data']['entries']
            ) if table_data.get('data', {}).get('entries', []) else 0
        
def normalization_index_regression(normalizations):
    h_array = []
    i_array = []
    j_array = []
    y_array = []
    for instance in normalizations:
        h_array.append(instance.aa_data.get('avg'))
        i_array.append(instance.mastery)
        j_array.append(1 if instance.skyfury else 0)
        y_array.append(instance.overall_dmg)
    h = np.array(h_array)
    i = np.array(i_array)
    j = np.array(j_array)
    X = np.column_stack((h,i,j))
    y = np.array(y_array)
    model = LinearRegression()
    model.fit(X,y)
    print("Intercept:", model.intercept_)
    print("Coefficient for melee:", model.coef_[0])
    print("Coefficient for mastery:", model.coef_[1])
    print("Coefficient for skyfury:", model.coef_[2])
    return model

def check_model(model, code, fight_id):
    instance = Normalization(code, fight_id)
    instance.dmg()
    prediction = model.predict(np.array([[instance.aa_data['avg'], instance.mastery, instance.skyfury]]))
    print("Predicted overall dmg:", prediction[0])
    
if __name__ == '__main__':
    test = Normalization('MF9fWYLPD2KRvpma', 5)
    test.length_index()
    # todo: test model