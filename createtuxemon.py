from tuxemon import Tuxemon
from moves import Attack
import json
import random
DIR = "~/tuxemongame/"

'''
This function creates a tuxemon as an Object of the Class Tuxemon
Txmns have different individual characteristics. 
Randomly, they have a 'nature' that give them different bonus on each Stat (hp, atk, spatk, deff, spdeff, spd),
different 'lvnature' that makes them need more or less Exp Points in order to Evolve and random Gender.
This make the game more diverse.
'''

def createTuxemon(TXMN, NATURE, LEVEL, LVNATURE):
    
    if NATURE == None:
        dicenature = random.randint(1,4)
        if dicenature == 1:
            nature = "calm"
        elif dicenature == 2:
            nature = "neutral"
        elif dicenature == 3:
            nature = "agile"
        else:
            nature = "agressive"
    else:
        nature = NATURE

    if LVNATURE == None:
        dicelvnature = random.randint(1,3)
        if dicelvnature == 1:
            lvnature = "idle"
        elif dicelvnature == 2:
            lvnature = "slow"
        else:
            lvnature = "fast"
    else:
        lvnature = LVNATURE

    with open(DIR+'tuxemons.json') as f:
        data1 = json.load(f)
        txmn = data1[TXMN]
    with open(DIR+'moves.json') as f:
        data2 = json.load(f)
        movesdict = data2
    with open(DIR+'movelist.json') as f:
        data3 = json.load(f)
        movelist = data3[TXMN]
    with open(DIR+'nature.json') as f:
        data4= json.load(f)
        naturelist = data4[nature]
    with open(DIR+'levels.json') as f:
        data5 = json.load(f)
        levelnature = data5[lvnature]
    
    ''' Getting txmn base stats infos '''

    name = txmn["name"]
    type1 = txmn["type1"]
    type2 = txmn["type2"]
    gender = txmn["gender"]

    basehp = txmn["basehp"]
    baseatk = txmn["baseatk"]
    basespatk = txmn["basespatk"]
    basedeff = txmn["basedeff"]
    basespdeff = txmn["basespdeff"]
    basespd = txmn["basespd"]  

    baseexp = txmn["baseexp"]   
    baselevel = txmn["baselevel"]

    ''' Getting txmn IV infos '''

    IVhp = naturelist["IVhp"]
    IVatk = naturelist["IVatk"]
    IVspatk = naturelist["IVspatk"]
    IVdeff = naturelist["IVdeff"]
    IVspdeff = naturelist["IVspdeff"]
    IVspd = naturelist["IVspd"]

    ''' Calculating the stats '''

    hp = int(((2 * basehp + IVhp) * LEVEL) / 4 + LEVEL + 10)
    currenthp = hp
    atk = int(((2 * baseatk + IVatk) * LEVEL) / 4 + LEVEL + 10)
    spatk = int(((2 * basespatk + IVspatk) * LEVEL) / 4 + LEVEL + 10)
    deff = int(((2 * basedeff + IVdeff) * LEVEL) / 4 + LEVEL + 10)
    spdeff = int(((2 * basespdeff + IVspdeff) * LEVEL) / 4 + LEVEL + 10)
    spd = int(((2 * basespd + IVspd) * LEVEL) / 4 + LEVEL + 10)

    ''' Setting what moves to learn by LEVEL '''
    
    moves = []
    available = list(movelist)
    if int(available[-1]) == LEVEL:  # Last move of the movelist
        index = len(movelist)-1
    else:
        for i in range(len(available)):
            if int(available[i]) > LEVEL:
                index = i-1
                break
    for i in range(index,index-4,-1):   # Filling moves of 4 index
        if i >= 0:
            if isinstance(movelist[available[i]], list):
                moves.append(movelist[available[i]][1])
                moves.append(movelist[available[i]][0])
            else:
                moves.append(movelist[available[i]])
        # Preparing the moves[] list with just 4 attacks
    for i in range(4,len(moves)):   # In case of more than 4 moves, reducing to only 4
        moves.pop()
    if len(moves) == 3:             # In case of only 3 moves, last move = None
        moves.append(None)
    elif len(moves) == 2:           # In case of only 2 moves, last two moves = None
        moves.append(None)
        moves.append(None)

    ''' Learning the Moves (as Objects) '''

    for i in range(4): # error
        if moves[i] == None:
            pass
        else:
            moves[i] = Attack(movesdict[moves[i]]["name"], movesdict[moves[i]]["power"], movesdict[moves[i]]["type"], movesdict[moves[i]]["hit"], movesdict[moves[i]]["accuracy"], movesdict[moves[i]]["pp"], movesdict[moves[i]]["effect"], movesdict[moves[i]]["effectChance"])

    ''' Setting last stats '''

    dice = random.randint(1,100)
    if dice < gender:
        gender = "Female"
    else:
        gender = "Male"

    exp = levelnature[str(LEVEL)]
    level = LEVEL
    effect = None
    item = None
    accuracy = 100

    return Tuxemon(name, type1, type2, gender, hp, currenthp, atk, spatk, deff, spdeff, spd, IVhp, IVatk, IVspatk, IVdeff, IVspdeff, IVspd, nature, exp, level, lvnature, effect, item, accuracy, moves)        
