import sys
import json
from random import shuffle

sys.path.append("../player")
sys.path.append("../card/")
from Player import Player
from RegionCard import RegionCard
from SanctuaryCard import SanctuaryCard
from Quest import Quest

class Board:

    NBOFREGIONCARDS = 68
    NBOFSANCTUARYCARDS = 45
    
    def __init__(self, players):
    

        self.RegionCardRevealed = []

        
        # Asserting we got a list of players to play with
        assert type(players) == list
        for i in players:
            assert type(i) == Player
        
        self.players = players
            
        # Initializing the region cards
        self.regionCards = []
        self.initializeRegionCards()
        shuffle(self.regionCards)

        # Initializing the sanctuary cards
        self.sanctuaryCards = []
        self.initializeSanctuaryCards()
        shuffle(self.sanctuaryCards)

    def initializeSanctuaryCards(self):
        with open("../../data/SanctuaryCards.json") as f:
            data = json.load(f)
            i = 0
            for line in data['sanctuaryCards']:
                i += 1
                id = str(line['id']).replace("sanctuary-", "")
                quest = Quest([], line['points'], line['conditionMode'], line['condition'])
                self.sanctuaryCards.append(SanctuaryCard(id, line['color'], quest, line['stones'], line['map'], line['night']))
            print(str(i) + " sanctuary cards has been successfully generated.")


    def initializeRegionCards(self):
        with open("../../data/RegionCards.json") as f:
            data = json.load(f)
            i = 0
            for line in data['regionCards']:
                i += 1
                id = str(line['id']).replace("region-", "")
                quest = Quest(line['require'], line['points'], line['conditionMode'], line['condition'])
                self.regionCards.append(RegionCard(id, line['color'], quest, line['stones'], line['map'], line['day']))
            print(str(i) + " region cards has been successfully generated.")
        


    def play(self):
        ## Setup of the game 
        for i in range(len(self.players)):
            for j in range(3):
                self.players[i].addCardToHand(self.regionCards.pop(0))

        while(len(self.players[0].revealedCards) < Player.NBCARDSTOREVEAL):
            for i in range(len(self.players)+1):
                self.RegionCardRevealed.append(self.regionCards.pop(0))

            starting = (self.players[0], Board.NBOFREGIONCARDS+1)
            for p in self.players:
                index = -1
                while(index <= 0 or index > Player.NBCARDSINHAND):
                    i=1
                    print("Player "+str(p.id)+" cards :")
                    for card in p.hand:
                        print(str(i)+" : "+card.toString())
                        i+=1
                    index = int(input("Player "+str(p.id)+" : Enter the index of the card you want to reveal : "))
                n = p.revealCard(index)
                if n < starting[1]:
                    starting = (p, n)
                print("Player "+str(p.id)+" has revealed "+p.revealedCards[-1].toString()+"\n")
                print("\n")

            
            indexP = self.players.index(starting[0])
            tmp = self.players[indexP]
            self.players[indexP] = self.players[0]
            self.players[0] = tmp

            for p in self.players:
                index=-1
                while(index <= 0 or index > len(self.players)+2):
                    i=1
                    print("Player "+str(p.id)+" cards :\n")
                    for card in self.RegionCardRevealed:
                        print(str(i)+" : "+card.toString())
                        i+=1
                    index = int(input("Player "+str(p.id)+" : Enter the index of the card you want to choose: "))
                card = self.RegionCardRevealed.pop(index-1)
                p.addCardToHand(card)
                print("Player "+str(p.id)+" has choose "+card.toString()+"\n")
                print("\n")

            self.RegionCardRevealed = []

        for p in self.players:
            print("Player "+str(p.id)+" final cards :")
            for c in p.revealedCards:
                print(c.toString())

        print("Game end\n")
        
        return