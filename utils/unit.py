class Player:
    def __init__(self, json):
        self.name = json['name']
        self.spec = json['specs'][0]['spec'] # todo: multispec solution
        self.id = json['id']
        self.region = json['region']
        self.class_ = json['type']
        self.combatantInfo = json['combatantInfo']
        
    def isSpec(self, spec):
        return self.spec == spec
    
    def isClass(self, cls):
        return self.class_ == cls