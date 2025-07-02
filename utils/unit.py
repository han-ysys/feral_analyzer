class Player:
    def __init__(self, json):
        self.name = json['name']
        self.spec = json['specs'][0]['spec'] # todo: multispec solution
        self.id = json['id']
        self.region = json['region']
        self.combatantInfo = json['combatantInfo']
        
    def isFeral(self):
        return self.spec == 'Feral'