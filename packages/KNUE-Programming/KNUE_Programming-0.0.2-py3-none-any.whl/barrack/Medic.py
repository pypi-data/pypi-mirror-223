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
            return print('May I Help You')
        if value == 'a':
            return print('Heal For You')
    