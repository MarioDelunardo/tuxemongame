from tuxemon import *
import random
import os
import time
from settings import *

'''
Those Effectiveness and Ineffectiveness Dictionaries need more implementation
'''

# Effectiveness Dictionary
rules = {   'Fire':'Grass',
            'Water':'Fire',
            'Grass':'Water',
            'Normal':None,
            'Dragon':'Dragon'}

# Ineffectiveness Dictionary
rulesrv = { 'Fire':'Water',
            'Water':'Grass',
            'Grass':'Fire',
            'Normal':None,
            'Dragon':'Dragon'}

# Health Bar Length
BARLENGTH = 30

def fight(tuxemon1, effectCounter1, tuxemon2, effectCounter2):
    '''
    This is the 'main function' that handle the battle. Here the attacks are choosed by the players
    and all the calculations involved (Damage, Hp loss, Effects, Accuracy dependent things) are done.
    '''
    hpUpdate(tuxemon1, tuxemon2)
    
    '''
    Player choosing an Attack
    '''
    while True:
        atk1 = tuxemon1.attack() - 1 # Player choose an attack between 1 and 4, but the index on moves[] are from 0 to 3, so atk = player_attack_choice - 1
        if tuxemon1.moves[atk1].pp > 0:
            break
        else: # No more PP on that move, so can't use it 
            time.sleep(FAST*TIME)
            print("No PP left!")
            print("Choose another move.")

    print()

    '''
    'IA' choosing an Attack (just random)
    '''
    counter = 0
    for i in range(4):  # removing eventual 'None' moves options from the random choice
        if tuxemon2.moves[i] == None:
            counter += 1
    randomatk = random.randint(0,3-counter)

    time.sleep(FAST*TIME)

    hpUpdate(tuxemon1, tuxemon2)
    
    DICE = random.randint(1,100)    # a 'general dice' used to determine all accuracy related decisions

    '''
    Deciding who attacks first
    In case one of Txmns uses Protection, that has high priority
    Otherwise, speed is the variable of decision. So faster Txmns attacks first
    '''
    if tuxemon1.moves[atk1].effect == "protect": # txmn1 used protect
        if doAttack(tuxemon1, DICE):
            doDamage(tuxemon1, atk1, tuxemon2, DICE)
            if tuxemon2.effect != None:
                handleEffect(tuxemon2, effectCounter2)
        
        hpUpdate(tuxemon1, tuxemon2)
        
        if tuxemon2.currenthp <= 0: # if txmn2 fainted
            return (tuxemon1, effectCounter1, tuxemon2, effectCounter2)    
        else:
            time.sleep(MID*TIME)
            print(tuxemon2.name + " used " + tuxemon2.moves[randomatk].name + ".")
            time.sleep(SLOW*TIME)
            print("No effect due to " + tuxemon1.name + " protection.")
            tuxemon2.moves[randomatk].pp = tuxemon2.moves[randomatk].pp - 1
            time.sleep(SLOW*TIME)
    
    elif tuxemon2.moves[randomatk].effect == "protect": # txmn2 used protect
        if doAttack(tuxemon2, DICE):
            doDamage(tuxemon2, randomatk, tuxemon1, DICE)
            if tuxemon1.effect != None:
                handleEffect(tuxemon1, effectCounter1)
        
        hpUpdate(tuxemon1, tuxemon2)
        
        if tuxemon1.currenthp <= 0: # if txmn1 fainted
            return (tuxemon1, effectCounter1, tuxemon2, effectCounter2)    
        else:
            time.sleep(MID*TIME)
            print(tuxemon1.name + " used " + tuxemon1.moves[atk1].name + ".")
            time.sleep(SLOW*TIME)
            print("No effect due to " + tuxemon2.name + " protection.")
            tuxemon1.moves[atk1].pp = tuxemon1.moves[atk1].pp - 1
            time.sleep(SLOW*TIME)
    
    elif tuxemon1.spd >= tuxemon2.spd:    # txmn1 is faster than txmn2
        if doAttack(tuxemon1, DICE):
            doDamage(tuxemon1, atk1, tuxemon2, DICE)
            if tuxemon1.moves[atk1].effect != None and DICE <= tuxemon1.moves[atk1].effectChance:
                doEffect(tuxemon1, atk1, tuxemon2)
                time.sleep(SLOW*TIME)
            if tuxemon2.effect != None:
                handleEffect(tuxemon2, effectCounter2)
                time.sleep(SLOW*TIME)
                
        hpUpdate(tuxemon1, tuxemon2)
        
        if tuxemon2.currenthp <= 0: # if txmn2 fainted
            return (tuxemon1, effectCounter1, tuxemon2, effectCounter2)    
        else:
            if doAttack(tuxemon2, DICE):
                doDamage(tuxemon2, randomatk, tuxemon1, DICE)
                if tuxemon2.moves[randomatk].effect != None and DICE <= tuxemon2.moves[randomatk].effectChance:
                    doEffect(tuxemon2, randomatk, tuxemon1)
                if tuxemon1.effect != None:
                    handleEffect(tuxemon1, effectCounter1)
                
        hpUpdate(tuxemon1, tuxemon2)  

    else:   # txmn2 is faster than txmn1
        if doAttack(tuxemon2, DICE):
            doDamage(tuxemon2, randomatk, tuxemon1, DICE)
            if tuxemon2.moves[randomatk].effect != None and DICE <= tuxemon2.moves[randomatk].effectChance:
                doEffect(tuxemon2, randomatk, tuxemon1)
                time.sleep(SLOW*TIME)
            if tuxemon1.effect != None:
                handleEffect(tuxemon1, effectCounter1)
                time.sleep(SLOW*TIME)

        hpUpdate(tuxemon1, tuxemon2)

        if tuxemon1.currenthp <= 0: # if txmn1 fainted
            return (tuxemon1, effectCounter1, tuxemon2, effectCounter2)
        else:
            if doAttack(tuxemon1, DICE):
                doDamage(tuxemon1, atk1, tuxemon2, DICE)
                if tuxemon1.moves[atk1].effect != None and DICE <= tuxemon1.moves[atk1].effectChance:
                    doEffect(tuxemon1, atk1, tuxemon2)
                if tuxemon2.effect != None:
                    handleEffect(tuxemon2, effectCounter2)
                
        hpUpdate(tuxemon1, tuxemon2)
    
    return(tuxemon1, effectCounter1, tuxemon2, effectCounter2)

def doAttack(txmn, dice):
    '''
    Calculate if the attack will hit or not
    '''
    if dice <= txmn.accuracy:
        if txmn.effect == "confusion":
            print(txmn.name + " is confused.")
            time.sleep(SLOW*TIME)
            if dice <= 40:
                print("It hit itself.")
                time.sleep(SLOW*TIME)
                txmn.currenthp = int(txmn.currenthp * 0.85)
        elif txmn.effect == "sleep":
            print("Shhhhhh... " + txmn.name + " is sleeping.")
            time.sleep(SLOW*TIME)
        elif txmn.effect == "flinch":
            print(txmn.name + " was flinched.")
            time.sleep(SLOW*TIME)
            txmn.effect = None
        else:
            return True
    else:
        print(txmn.name + " missed the attack.")
        time.sleep(SLOW*TIME)
    return False

def doDamage(t1, atk, t2, dice):
    '''
    Calculate the damage of the attack
    '''
    time.sleep(MID*TIME)
    print(t1.name + " used " + t1.moves[atk].name + ".")
    time.sleep(SLOW*TIME)
    
    if t1.moves[atk].effect == "critical" and dice <= t1.moves[atk].effectChance: # moves that has high critical rate
        CRIT = 1.2
        print("Critical hit")
    elif dice <= 10:    # normal critical rate moves
        CRIT = 1.2
        print("Critical hit")
    else:   # no crit
        CRIT = 1
    
    # Damages multipliers
    LOW = 0.5
    NORMAL = 1.0
    HIGH = 1.5

    if t2.type1 == t2.type2:
        if t1.moves[atk].type == t2.type1 or t1.moves[atk].type == rules[t2.type1]:
            print("It's not very effective...")
            if t1.moves[atk].hit == "Physical":
                t2.currenthp = int(t2.currenthp - CRIT * LOW * ((t1.moves[atk].power + t1.level) * (t1.atk + t1.spatk * 0.5)/(t2.deff + t2.spdeff * 0.5)))
            elif t1.moves[atk].hit == "Special":
                t2.currenthp = int(t2.currenthp - CRIT * LOW * ((t1.moves[atk].power + t1.level) * (t1.spatk + t1.atk * 0.5)/(t2.spdeff + t2.deff * 0.5)))
            else: # Status hit type
                pass
        elif t1.moves[atk].type == rulesrv[t2.type1]:
            print("It's super effective!")
            if t1.moves[atk].hit == "Physical":
                t2.currenthp = int(t2.currenthp - CRIT * HIGH * ((t1.moves[atk].power + t1.level) * (t1.atk + t1.spatk * 0.5)/(t2.deff + t2.spdeff * 0.5)))
            elif t1.moves[atk].hit == "Special":
                t2.currenthp = int(t2.currenthp - CRIT * HIGH * ((t1.moves[atk].power + t1.level) * (t1.spatk + t1.atk * 0.5)/(t2.spdeff + t2.deff * 0.5)))
            else: # Status hit type
                pass
        else:
            #print("Normal hit")
            if t1.moves[atk].hit == "Physical":
                t2.currenthp = int(t2.currenthp - CRIT * NORMAL * ((t1.moves[atk].power + t1.level) * (t1.atk + t1.spatk * 0.5)/(t2.deff + t2.spdeff * 0.5)))
            elif t1.moves[atk].hit == "Special":
                t2.currenthp = int(t2.currenthp - CRIT * NORMAL * ((t1.moves[atk].power + t1.level) * (t1.spatk + t1.atk * 0.5)/(t2.spdeff + t2.deff * 0.5)))
            else: # Status hit type
                pass
    else:
        if t1.moves[atk].type == t2.type1 or t1.moves[atk].type == t2.type2 or t1.moves[atk].type == rules[t2.type2] or t1.moves[atk].type == rules[t2.type2]:
            print("It's not very effective...")
            if t1.moves[atk].hit == "Physical":
                t2.currenthp = int(t2.currenthp - CRIT * LOW * (t1.moves[atk].power * (t1.atk + t1.spatk * 0.5)/(t2.deff + t2.spdeff * 0.5)))
            elif t1.moves[atk].hit == "Special":
                t2.currenthp = int(t2.currenthp - CRIT * LOW * (t1.moves[atk].power * (t1.spatk + t1.atk * 0.5)/(t2.spdeff + t2.deff * 0.5)))
            else: # Status hit type
                pass
        elif t1.moves[atk].type == rulesrv[t2.type1] or t1.moves[atk-1].type == rulesrv[t2.type2]:
            print("It's super effective!")
            if t1.moves[atk].hit == "Physical":
                t2.currenthp = int(t2.currenthp - CRIT * HIGH * (t1.moves[atk].power * (t1.atk + t1.spatk * 0.5)/(t2.deff + t2.spdeff * 0.5)))
            elif t1.moves[atk].hit == "Special":
                t2.currenthp = int(t2.currenthp - CRIT * HIGH * (t1.moves[atk].power * (t1.spatk + t1.atk * 0.5)/(t2.spdeff + t2.deff * 0.5)))
            else: # Status hit type
                pass
        else:
            #print("'Normal hit'")
            if t1.moves[atk].hit == "Physical":
                t2.currenthp = int(t2.currenthp - CRIT * NORMAL * (t1.moves[atk].power * (t1.atk + t1.spatk * 0.5)/(t2.deff + t2.spdeff * 0.5)))
            elif t1.moves[atk].hit == "Special":
                t2.currenthp = int(t2.currenthp - CRIT * NORMAL * (t1.moves[atk].power * (t1.spatk + t1.atk * 0.5)/(t2.spdeff + t2.deff * 0.5)))
            else: # Status hit type
                pass
    
    # Lowering PP
    t1.moves[atk].pp = t1.moves[atk].pp - 1

    time.sleep(SLOW*TIME)

def doEffect(t1, atk, t2):
    if t1.moves[atk].effect == "burn":
        t2.effect = "burn"
        print(t2.name + " was burned.")
    elif t1.moves[atk].effect == "leechseed":
        t2.effect = "leechseed"
    elif t1.moves[atk].effect == "poison":
        t2.effect = "poison"
        print(t2.name + " was poisoned.")
    elif t1.moves[atk].effect == "sleep":
        t2.effect = "sleep"
        print("Shhhhhh... " + t2.name + " is now sleeping.")
    elif t1.moves[atk].effect == "paralyse":
        t2.effect = "paralyse"
        print(t2.name + " was paralysed.")
    elif t1.moves[atk].effect == "flinch": # need more implementation
        t2.effect = "flinch"
        print(t2.name + " was flinched.") 
    elif t1.moves[atk].effect == "confusion":
        t2.effect = "confusion"
        print(t2.name + " is now confused.")
    elif t1.moves[atk].effect == "protect": # need more implementation
        t1.effect = "protect"
    elif t1.moves[atk].effect == "decOpAtk":
        t2.atk = t2.atk - 10
        print(t2.name + " Attack fell.")
    elif t1.moves[atk].effect == "decOpAcc":
        t2.accuracy = t2.accuracy - 10
        print(t2.name + " Accuracy fell.")
    elif t1.moves[atk].effect == "decOpDeff":
        t2.deff = t2.deff - 10
        print(t2.name + " Defense fell.")
    elif t1.moves[atk].effect == "incDeff":
        t1.deff = t1.deff + 10
        print(t1.name + " Defense rose.")
    elif t1.moves[atk].effect == "incSpAtk":
        t1.spatk = t1.spatk + 10
        print(t1.name + " Special Attack rose.")
    
def handleEffect(txmn, counter):
    '''
    Handle effects that persists for more than one round
    '''
    if txmn.effect == "burn":
        if counter == 4:
            print(txmn.name + " is no longer burning.")
            txmn.effect = None
        else:
            print(txmn.name + " damaged by burn.")
            txmn.currenthp = int(txmn.currenthp * 0.95)
    elif txmn.effect == "poison":
        if counter == 4:
            print(txmn.name + " is no longer poisoned.")
            txmn.effect = None
        else:
            print(txmn.name + " damaged by poison.")
            txmn.currenthp = int(txmn.currenthp * 0.95)
    elif txmn.effect == "sleep" and counter == 4:
            print(txmn.name + " woke up.")
            txmn.effect = None
    elif txmn.effect == "confusion" and counter == 4:
            print(txmn.name + " is on longer confused.")
            txmn.effect = None
    elif txmn.effect == "paralyse" and counter == 4:
            print(txmn.name + " is paralysed.")
            txmn.effect = None

def hpUpdate(t1, t2):    
    '''
    Draws the health bars of the tuxemons in the battle
    '''
    os.system('cls||clear')
    if t1.currenthp <= 0: 
        print(t1.name + " health: 0")
    else:
        print(t1.name + " health: " + str(t1.currenthp))
    barvec = ["["]
    barstr = "["
    draw = int(BARLENGTH * t1.currenthp/t1.hp)
    if draw == 0 and t1.currenthp > 0:
        barvec.append("=")
    else:
        for i in range(draw):
            barvec.append("=")
        for i in range(draw,BARLENGTH):
            barvec.append(" ")
        barvec.append("]")
        for i in range(1,BARLENGTH+1):
            barstr += str(barvec[i])
    barstr += "]"
    print(barstr)
    
    if t1.effect == None:
        print("St: ---")
    elif t1.effect == "paralyze":
        print("St: PAR")
    elif t1.effect == "poison":
        print("St: PSN")
    elif t1.effect == "sleep":
        print("St: SLP")
    elif t1.effect == "burn":
        print("St: BRN")
    
    print()

    if t2.currenthp <= 0: 
        print(t2.name + " health: 0")
    else:
        print(t2.name + " health: " + str(t2.currenthp))
    barvec = ["["]
    barstr = "["
    draw = int(BARLENGTH * t2.currenthp/t2.hp)
    if draw == 0 and t2.currenthp > 0:
        barvec.append("=")
    else:
        for i in range(draw):
            barvec.append("=")
        for i in range(draw,BARLENGTH):
            barvec.append(" ")
        barvec.append("]")
        for i in range(1,BARLENGTH+1):
            barstr += str(barvec[i])
    barstr += "]"
    print(barstr)

    if t2.effect == None:
        print("St: ---")
    elif t2.effect == "paralyze":
        print("St: PAR")
    elif t2.effect == "poison":
        print("St: PSN")
    elif t2.effect == "sleep":
        print("St: SLP")
    elif t2.effect == "burn":
        print("St: BRN")

    print()