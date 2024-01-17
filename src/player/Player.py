import sys

sys.path.append("../card")
sys.path.append("../game")

from RegionCard import RegionCard
from SanctuaryCard import SanctuaryCard

from Board import *




class Player:
    
    NBCARDSINHAND = 3
    NBCARDSTOREVEAL = 8
    
    def __init__(self, id):
        self.hand = []
        self.revealedCards = []
        self.sanctuaryCards = []
        self.handSanctuary = []
        self.id = id
    
    
    def addCardToHand(self, x):
        if type(x) != RegionCard:  #Trying to add something that is not a region card in the player hand
            print("Error : cannot add anything but a region card in the player's hand.")
            return
        
        if len(self.hand) < Player.NBCARDSINHAND :
                self.hand.append(x)
        else:
            print("Error : the hand of the player " + str(self.id) + " is full.")

    def addCardToHandSanctuary(self, x):
        if type(x) != SanctuaryCard:  #Trying to add something that is not a region card in the player hand
            print("Error : cannot add anything but a region card in the player's hand.")
            return
        self.hand.append(x)


    
    def revealCard(self, index): #The index choosed cannot be 0 (starting at 1)
        if index <= 0 or index > len(self.hand):
            print("Error : the index choosed in incorrect, please retry.")
            sys.exit()
        else:
            card = self.hand.pop(index-1)
            self.revealedCards.append(card)
            return int(card.id)
        


    def canRevealCard(self):
        return len(self.revealedCards) < Player.NBCARDSTOREVEAL
            
            
