from settings import *
from player import *
import os
import time

'''
State of the Game: Creating Player character and Rival character
Both are created as Objects of Player class
'''

def introState():
    introText()

    os.system('cls||clear')

    '''
    Creating the Player character 
    '''
    name = input("What is your name? ")
    while True:
        choice = int(input("Your name is " + name + "? (1-Y | 2-N)"))
        if choice == 2:
            os.system('cls||clear')
            name = input("What is your name?")
        else:
            os.system('cls||clear')
            break
    
    gender = int(input("Are you a Boy or a Girl? (1-Boy | 2-Girl)"))
    while True:
        if gender == 1:
            choice = int(input("So you are a boy? (1-Y | 2-N)"))
            if choice == 2:
                os.system('cls||clear')
                gender = int(input("Are you a Boy or a Girl? (1-Boy | 2-Girl)"))
            else:
                gender = "boy"
                break
        elif gender == 2:
            choice = int(input("So you are a girl? (1-Y | 2-N)"))
            if choice == 2:
                os.system('cls||clear')
                gender = int(input("Are you a Boy or a Girl? (1-Boy | 2-Girl)"))
            else:
                gender = "girl"
                break

    team = []
    bag = []

    player = Player(name, gender, team, bag)

    '''
    Creating the Rival character
    '''
    if player.gender == "boy":
        rival = Player("Misty", "girl", [], [])
    else:
        rival = Player("Ash", "boy", [], [])

    return(player, rival)

def introText():
    print("Welcome to Tuxemon Game!!")
    time.sleep(FAST*TIME)
    print("A little project by someone who likes programming and Pokémons")
    time.sleep(FAST*TIME)
    print("...")
    time.sleep(FAST*TIME)
    print("I mean...")
    time.sleep(SLOW*TIME)
    print("Tuxemons!!")
    time.sleep(FAST*TIME)
    print("No lawsuits, Nintendo :)")

    os.system('cls||clear')

    print("Lets go to what matters")
    time.sleep(FAST*TIME)
    print("Battles!!")
    time.sleep(SLOW*TIME)
    print("But first...")
    time.sleep(FAST*TIME)