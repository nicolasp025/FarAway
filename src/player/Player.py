import sys

sys.path.append("../card")
sys.path.append("../game")

from Card import *

from Board import *




class Player:
    
    NBCARDSINHAND = 3
    NBCARDSTOREVEAL = 8
    
    def __init__(self, id):
        self.hand = []
        self.revealedCards = []
        self.sanctuaryCards = []
        self.id = id
    
    
    def addCardToHand(self, x):
        if type(x) != RegionCard:  #Trying to add something that is not a region card in the player hand
            print("Error : cannot add anything but a region card in the player's hand.")
            return
        
        if len(self.hand) < NBCARDSINHAND :
                self.hand.append(x)
        else:
            print("Error : the hand of the player " + str(self.id) + " is full.")


    
    def revealCard(index): #The index choosed cannot be 0 (starting at 1)
        if index <= 0 or index > len(self.hand):
            print("Error : the index choosed in incorrect, please retry.")
            sys.exit()
            
        


    def canRevealCard():
        return len(self.revealedCards) < NBCARDSTOREVEAL
            
            
