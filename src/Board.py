from Player import *

class Board:
    
    def __init__(self, players):
        
        NBOFREGIONCARDS = 68
        NBOFSANCTUARYCARDS = 45
        
        # Asserting we got a list of players to play with
        assert type(players) == list
        for i in players:
            assert type(i) == Player
        
        self.players = players
            
        # Initializing the region cards
        self.regionCards = []
        for i in range(NBOFREGIONCARDS):
            
            self.regionCards.append(RegionCard(i+1))
        print(self.regionCards)
        # Initializing the sanctuary cards
        
    def play(self):
        pass