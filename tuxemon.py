from moves import *
import json

'''
Define the Tuxemon class
'''

class Tuxemon:
    def __init__(self, name, type1, type2, gender, hp, currenthp, atk, spatk, deff, spdeff, spd, IVhp, IVatk, IVspatk, IVdeff, IVspdeff, IVspd, nature, exp, level, lvnature, effect, item, accuracy, moves):
        self.name = name
        self.type1 = type1
        self.type2 = type2        
        self.gender = gender

        self.hp = hp
        self.currenthp = currenthp
        self.atk = atk
        self.spatk = spatk 
        self.deff = deff
        self.spdeff = spdeff 
        self.spd = spd
        
        self.IVhp = IVhp
        self.IVatk = IVatk
        self.IVspatk = IVspatk
        self.IVdeff = IVdeff
        self.IVspdeff = IVspdeff
        self.IVspd = IVspd
        
        self.nature = nature
        self.exp = exp
        self.level = level
        self.lvnature = lvnature

        self.effect = effect 
        self.item = item
        self.accuracy = accuracy
        self.moves = moves

    def attack(self):
        print(self.name + " knows these moves: ")
        for i in range(len(self.moves)):
            if self.moves[i] == None:
                pass
            else:
                print(str(i+1) + ' - ' + str.upper(self.moves[i].name))
                print("| Power: " + str(self.moves[i].power) + " | Type: " + self.moves[i].type + " " + str.casefold( self.moves[i].hit) + " attack")
                print("| PP: " + str(self.moves[i].pp) + " | Accuracy: " + str(self.moves[i].accuracy) +"\n")
        while True:
            self.choose = input("Choose a move to use: ")
            for i in range(len(self.moves)):
                if self.choose == str(i+1):
                    return int(self.choose)
            print("Invalid choice!")
    
    def lvup(self):
        self.level = self.level + 1
        self.hp = self.hp + 2 * (5 + self.IVhp)
        self.atk = self.atk + 2 * (5 + self.IVatk)
        self.spatk = self.spatk + 2 * (5 + self.IVspatk)
        self.deff = self.deff + 2 * (5 + self.IVdeff)
        self.spdeff = self.spdeff + 2 * (5 + self.IVspdeff)
        self.spd = self.spd + 2 * (5 + self.IVspd)

    def evolve(evolve):
        with open('tuxemons.json') as f:
            data = json.load(f)
            txmn = data[evolve]
        self.name = txmn["name"]
        self.type1 = txmn["type1"]
        self.type2 = txmn["type2"]
        # Bonus stats
        self.hp = self.hp + 5
        self.atk = self.atk + 5
        self.spatk = self.spatk + 5
        self.deff = self.deff + 5
        self.spdeff = self.spdeff + 5
        self.spd = self.spd + 5