'''
Define the Attack class
'''

class Attack:
    def __init__(self, name, power, type, hit, accuracy, pp, effect, effectChance):
        self.name = name
        self.power = power
        self.type = type
        self.hit = hit
        self.accuracy = accuracy
        self.pp = pp
        self.effect = effect
        self.effectChance = effectChance