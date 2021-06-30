from introState import *
from starterState import *
from fightState import *
from player import *
from tuxemon import *
import os
import time
from settings import *

'''
The main file handles the States of the Game.
Basically, the Game has a List filled with possible States and runs the last one.
So using 'append' and 'pop' make the transitions between States very easy.
'''

def main():
    gameState = []
    gameState.append("quit")
    gameState.append("intro")

    while True: # run always the last State on the gameState List
        if gameState[-1] == "quit":
            break
        elif gameState[-1] == "intro":
            os.system('cls||clear')
            characters = introState()
            player = characters[0]
            rival = characters[1]
            gameState.pop()
            gameState.append("starter")        
        elif gameState[-1] == "fight":
            os.system('cls||clear')
            winner = fightState(playerStarter, rivalStarter)
            print("The battle is over.")
            time.sleep(FAST*TIME)
            if winner == "txmn1": # need more implementation. maybe an 'endBattleState'
                print(rivalStarter.name + " fainted")
                time.sleep(SLOW*TIME)
                os.system('cls||clear')
                print("You won the battle!!")
            elif winner == "txmn2":
                print(playerStarter.name + " fainted")
                time.sleep(SLOW*TIME)
                os.system('cls||clear')
                print("You lost the battle...")
            gameState.pop()            
        elif gameState[-1] == "starter":
            os.system('cls||clear')
            starters = starterState()
            playerStarter = starters[0]
            rivalStarter = starters[1]
            player.team.append(playerStarter)
            rival.team.append(rivalStarter)
            gameState.pop()
            gameState.append("fight")
        elif gameState[-1] == "settings": # need more implementation
            pass

    print("Thanks for playing :)")

if __name__ == '__main__':
    main()
