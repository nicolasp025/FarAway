import sys
sys.path.append("./src/game/")
import Board
from Board import Board
from BoardDisplay import BoardDisplay

sys.path.append("./src/player/")
import Player
from Player import Player

MINIMUMPLAYERS = 2
MAXIMUMPLAYERS = 6

def start():
    # Getting the number of players
    print("How many players do you want to play with ?")
    nbPlayers = int(input("Number of players should be between "+ str(MINIMUMPLAYERS) + " and " + str(MAXIMUMPLAYERS) + " : "))
    
    if nbPlayers < MINIMUMPLAYERS or nbPlayers > MAXIMUMPLAYERS:
        print("Error: the specified number of players is incorrect, please restart.")
        return
    
    # Generate all the players
    players = []
    for i in range(nbPlayers):
        players.append(Player(i))
    print("The " + str(nbPlayers) + " players has been successfully created.")
    
    board = Board(players)
    board.play()

def play():

    args = sys.argv 

    if len(args)>1:
        if args[1] == '-d':
            board = BoardDisplay()
            board.play()
        else:
            start()
    else:
        start()
    

    

if __name__ == "__main__":
    play()
    
    