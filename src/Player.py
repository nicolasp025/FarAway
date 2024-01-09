from Card import *

import sys



class Player:
    
    NBCARDSINHAND = 3
    NBCARDSTOREVEAL = 8
    
    def __init__(self, id):
        self.hand = []
        self.revealedCards = []
        self.sanctuaryCards = []
        self.id = id
        print("The player " + str(id) + " has been successfully inialized.")
    
    
    
    def addCardToHand(x):
        if type(x) != RegionCard:  #Trying to add something that is not a region card in the player hand
            print("Error : cannot add anything but a region card in the player's hand.")
            sys.exit()
        
        if len(self.hand) < NBCARDSINHAND :
                self.hand.append(x)
        else:
            print("Error : the hand of the player " + str(self.id) + " is full.")

    
    def 


    def canRevealCard():
        return len(self.revealed_cards) < NBCARDSTOREVEAL
            
            
            
            
            
            
            
players = [Player(i+1) for i in range(4)]
cards = [Card(i) for i in range(5)]        
            
