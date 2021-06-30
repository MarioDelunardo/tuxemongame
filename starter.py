from tuxemon import *
from createtuxemon import *
import time
import os
from settings import *

'''
Handle the starter choice of the player.
In future implementation should be moved to starterState
'''

def choose_txmn():
    choosed = False
    while not choosed:
        os.system('cls||clear')
        txmn = input("Choose between 1-Tweesher, 2-Agnite or 3-Anoleaf: ")
        if txmn == '1':
            choosed = explain(1)
        elif txmn == '2':
            choosed = explain(2)
        elif txmn == '3':
            choosed = explain(3)
        else:
            print("Invalid choice!")

    if txmn == '1':
        return createTuxemon("tweesher", None, 5, None)
    elif txmn == '2':
        return createTuxemon("agnite", None, 5, None)
    elif txmn == '3':
        return createTuxemon("anoleaf", None, 5, None)

def explain(num):
    time.sleep(.7*TIME)
    if num == 1:
        print("Tweesher is a Water type Tuxemon.")
        print("Tuxemons of that type are good against Fire types, and not so good agains Grass types.")
    elif num == 2:
        print("Agnite is a Fire type Tuxemon")
        print("Tuxemons of that type are good against Grass types, and not so good agains Water types.")
    else:
        print("Anoleaf is a Grass type Tuxemon") 
        print("Tuxemons of that type are good against Water types, and not so good agains Fire types.")
    time.sleep(.7*TIME)

    choice = input("\nWant to choose it? (1-Y | 2-N) ")
    while True:
        if choice == '1':
            return True
        elif choice == '2':
            return False
        else:
            print("Invalid choice!")