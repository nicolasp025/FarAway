from Board import *
from Player import *

import sys

def play():
    board = Board()
    
    MINIMUMPLAYERS = 2
    MAXIMUMPLAYERS = 6
    
    print("How many players do you want to play with ?")
    nbPlayers = int(input("Number of players should be between "+ str(MINIMUMPLAYERS) + " and " + str(MAXIMUMPLAYERS) + " : "))
    
    if nbPlayers < MINIMUMPLAYERS or nbPlayers > MAXIMUMPLAYERS:
        print("Error: the specified number of players is incorrect, please restart.")
        return
    
    players = []
    for i in range(nbPlayers):
        players.append(Player(i))
    print("The players has been successfully created.")
    
    

if __name__ == "__main__":
    play()
    
    