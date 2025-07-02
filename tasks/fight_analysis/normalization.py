from utils import catcher, unit
import json

class Normalization:
    def __init__(self, code, ids, source_id=None):
        self.code = code
        self.ids = ids
        if not source_id:
            players = catcher.player_data(code, ids)
            for player_json in players['dps']:
                player = unit.Player(player_json)
                if player.isFeral:
                    self.source_id = player.id
        
    def length_index(self):
        aa = catcher.table_data(self.code, fight_ids=self.ids, source_id=self.source_id, ability_id=1)
        with open('data_json/aa_data.json', 'w') as f:
            json.dump(aa, f, indent=4)
        # todo
        
if __name__ == '__main__':
    test = Normalization('MF9fWYLPD2KRvpma', 5)
    test.length_index()