from Player import *
from RegionCard import *
import json
from SanctuaryCard import SanctuaryCard
from Quest import Quest

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
        self.initializeRegionCards()

        # Initializing the sanctuary cards
        self.sanctuaryCards = []
        self.initializeSanctuaryCards()

    def initializeSanctuaryCards(self):
        f = open("../data/SanctuaryCards.json", )
        data = json.load(f)
        i = 0
        for line in data['sanctuaryCards']:
            i += 1
            id = str(line['id']).replace("sanctuary-", "")
            quest = Quest([], line['points'], line['conditionMode'], line['condition'])
            self.sanctuaryCards.append(SanctuaryCard(id, line['color'], quest, line['stones'], line['map'], line['night']))
        print(str(i) + " sanctuary cards has been successfully generated.")
        f.close()


    def initializeRegionCards(self):
        f = open("../data/RegionCards.json", )
        data = json.load(f)
        i = 0
        for line in data['regionCards']:
            i += 1
            id = str(line['id']).replace("region-", "")
            quest = Quest(line['require'], line['points'], line['conditionMode'], line['condition'])
            self.regionCards.append(RegionCard(id, line['color'], quest, line['stones'], line['map'], line['day']))
        print(str(i) + " region cards has been successfully generated.")
        f.close()


    def play(self):
        pass