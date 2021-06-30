from starter import *
from tuxemon import *
import os
import time
from settings import *

'''
State of the Game: Choosing Starter
'''

def starterState():
    playerStarter=choose_txmn()
    print("First Tuxemon choosed.\n")

    time.sleep(SLOW*TIME)

    if playerStarter.name == "Tweesher":   # Forced to battle against stronger type
        rivalStarter = createTuxemon("anoleaf", None, 5, None)
    elif playerStarter.name == "Agnite":
        rivalStarter = createTuxemon("tweesher", None, 5, None)
    else:
        rivalStarter = createTuxemon("agnite", None, 5, None)

    print(rivalStarter.name + " will be your opponent.\n")

    print(".")
    time.sleep(FAST*TIME)
    print(".")
    time.sleep(FAST*TIME)
    print(".\n")
    time.sleep(FAST*TIME)
    print("Let's battle!!!")
    time.sleep(SLOW*TIME)

    return(playerStarter, rivalStarter)