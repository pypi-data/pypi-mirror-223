from barrack import HP, MP


class Medic:
    species = 'Terran'
    
    def __init__(self, location, upgrade, hp=HP, mp=MP):
      self.location = location
      self.upgrade = upgrade
      self.hp = hp
      self.mp = mp
	
        
    def click(self, value=None):
        if value == None:
            return print('You will die')
        if value == 'a':
            return print('I will help you')
    