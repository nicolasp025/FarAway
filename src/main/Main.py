import sys
sys.path.append("./src/game/")
from BoardClassical import BoardClassical
from BoardDisplay import BoardDisplay
        

def play() -> None:
    args = sys.argv 

    # If the user wants to play with the display
    if len(args)>1:
        if args[1] == '-d':
            board = BoardDisplay()
            board.play()
    else:
        board = BoardClassical()
        board.play()
    

if __name__ == "__main__":
    play()
    
    