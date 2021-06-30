from tuxemon import *
from fight import *

'''
State of the Game: Fighting
'''

def fightState(txmn1, txmn2):
    '''
    Handle the duration of the Effects and if the battle has a winner  
    '''
    winner = ""
    effectCounter1 = 0
    effectCounter2 = 0

    while True:
        fightSituation=fight(txmn1, effectCounter1, txmn2, effectCounter2)
        
        if fightSituation[0].currenthp <= 0:
            print(txmn1.name + " fainted")            
            winner = "txmn2"
            return winner
        elif fightSituation[2].currenthp <= 0:
            print(txmn2.name + " fainted")
            winner = "txmn1"
            return winner

        if fightSituation[0].effect != None:
            effectCounter1 = effectCounter1 + 1
            if effectCounter1 > 4:
                effectCounter1 = 0
        if fightSituation[2].effect != None:
            effectCounter2 = effectCounter2 + 1
            if effectCounter2 > 4:
                effectCounter2 = 0