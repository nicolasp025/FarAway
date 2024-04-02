import sys

sys.path.append("./src/card")

from RegionCard import RegionCard
from SanctuaryCard import SanctuaryCard

class Player:
    
    NBCARDSINHAND = 3
    NBCARDSTOREVEAL = 8
    
    def __init__(self, id):
        self.hand = []
        self.revealedCards = []
        self.sanctuaryCards = []
        self.id = id
        self.pseudo = ""
    
    
    def addCardToHand(self, x):
        if type(x) != RegionCard:  #Trying to add something that is not a region card in the player hand
            print("Error : cannot add anything but a region card in the player's hand.")
            return
        
        if len(self.hand) < Player.NBCARDSINHAND :
                self.hand.append(x)
        else:
            print("Error : the hand of the player " + str(self.id) + " is full.")

    def addCardToSanctuaryCards(self, x):
        if type(x) != SanctuaryCard:  #Trying to add something that is not a region card in the player hand
            print("Error : cannot add anything but a region card in the player's hand.")
            return
        self.sanctuaryCards.append(x)

    def addPseudo(self, pseudo:str) -> None:
        self.pseudo = pseudo
    
    def revealCard(self, index): #The index choosed cannot be 0 (starting at 1)
        if index <= 0 or index > len(self.hand):
            print("Error : the index choosed is incorrect, please retry.")
            return 
        else:
            card = self.hand.pop(index-1)
            self.revealedCards.append(card)
            return int(card.id) ## return the id of the card revealed
        
    def sanctuaryCardToAdd(self):
        res = 0
        if len(self.revealedCards) < 2:
            return res
        if self.revealedCards[-1].id > self.revealedCards[-2].id:
            res += 1
            for rCard in self.revealedCards:
                if rCard.map:
                    res += 1
            for sCard in self.sanctuaryCards:
                if sCard.map:
                    res += 1
        return res
        
            
            
