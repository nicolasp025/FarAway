import sys
import json
from random import shuffle

sys.path.append("./src/player/")
sys.path.append("./src/card/")
sys.path.append("./src/enum/")

from Board import Board
from Colors import Colors
from Quest import Quest
from Stones import Stones
from Player import Player
from RegionCard import RegionCard
from SanctuaryCard import SanctuaryCard
from ConditionModes import ConditionModes

class BoardClassical(Board):

    def __init__(self):

        super().__init__()


    def chooseNbPlayers(self):
        # Getting the number of players
        print("How many players do you want to play with ?")
        nbPlayers = int(input("Number of players should be between "+ str(super().MINIMUMPLAYERS) + " and " + str(super().MAXIMUMPLAYERS) + " : "))
        
        if nbPlayers < super().MINIMUMPLAYERS or nbPlayers > super().MAXIMUMPLAYERS:
            print("Error: the specified number of players is incorrect, please restart.")
            return
        
        # Generate all the players
        for i in range(nbPlayers):
            self.players.append(Player(i+1))
        print("The " + str(nbPlayers) + " players has been successfully created.")
    
        print("----------------- Start of the Game ------------------- \n\n")
        ## Setup of the game 
        for i in range(len(self.players)):
            for j in range(3):
                self.players[i].addCardToHand(self.regionCards.pop(0))
                

    def chooseCardToReveal(self):
        ### Choose the card to reveal
        print("----------------- Turn number "+str(self.nbTurns+1)+" -----------------\n")

        print("----------------- Choose the card you want to reveal ------------------- \n")
        starting = []
        for p in self.players:
            index = -1
            while(type(index) != int or index <= 0 or index > Player.NBCARDSINHAND):
                i=1
                print("Player "+str(p.id)+" cards :")
                for card in p.hand:
                    print(str(i)+" : "+card.toString())
                    i+=1
                inp = input("Player "+str(p.id)+" : Enter the index of the card you want to reveal : ")
                if str.isdigit(inp):
                    index = int(inp)
            n = p.revealCard(int(index))
            starting.append((p, n))
            print("Player "+str(p.id)+" has revealed "+p.revealedCards[-1].toString()+"\n")
            print("\n")
            ## Set the new list of player with the right order 
            starting.sort(key=lambda x : x[1])
            self.players = [t[0] for t in starting]

    
    def chooseSanctuaryCard(self):
        print("----------------- Choose the sanctuary card you want to add to your hand  ------------------- \n")
        ## Choose sanctuary card if you had to
        for p in self.players:
            nbToAdd = p.sanctuaryCardToAdd()
            if nbToAdd > 0:
                self.checkSanctuaryCards(nbToAdd)
                print("Player "+str(p.id)+" sanctuary cards available :")
                index = -1
                while(type(index) != int or index <= 0 or index > nbToAdd):
                    for i in range(1, nbToAdd+1):
                        print(str(i)+" : "+self.sanctuaryCards[i-1].toString())
                    inp = input("Player "+str(p.id)+" : Enter the index of the sanctuary card you want to take : ")
                    if str.isdigit(inp):
                        index = int(inp)
                p.addCardToSanctuaryCards(self.sanctuaryCards.pop(index-1))
                for i in range(nbToAdd-1):
                    self.sanctuaryCardsUsed.append(self.sanctuaryCards.pop(0))
                print("Player "+str(p.id)+" has taken "+p.sanctuaryCards[-1].toString()+"\n")
                print("\n")


    def chooseRegionCard(self):
        if (self.nbTurns < 7):
            for i in range(len(self.players)+1):
                self.RegionCardRevealed.append(self.regionCards.pop(0))
            print("----------------- Choose the region card you want to add to your hand  ------------------- \n")
            ## Choose the region card for player hand
            for p in self.players:
                index = -1
                while(type(index) != int or index <= 0 or index > len(self.players)+2):
                    i=1
                    print("All cards available :\n")
                    for card in self.RegionCardRevealed:
                        print(str(i)+" : "+card.toString())
                        i+=1
                    inp = input("Player "+str(p.id)+" : Enter the index of the card you want to choose: ")
                    if str.isdigit(inp):
                        index = int(inp)
                card = self.RegionCardRevealed.pop(index-1)
                p.addCardToHand(card)
                print("Player "+str(p.id)+" has choose "+card.toString()+"\n")
                print("\n")

    def displayEnd(self):
        print("----------------- Final Cards for each player  ------------------- \n")
        ## Print final cards revealed by players
        for p in self.players:
            print("Player "+str(p.id)+" final cards :")
            for c in p.revealedCards:
                print(c.toString())
                
        print("------------ Counting points ------------")
        winner = (0, 0)
        for p, res in self.countFinalPoints().items():
            print("Player "+str(p)+" : "+str(res)+" points\n")
            if res > winner[1]:
                winner = (p, res)
        print("Winner : Player "+str(winner[0])+"\n")
        print("Game end\n")


    def play(self):
        self.chooseNbPlayers()
        while(self.nbTurns < Player.NBCARDSTOREVEAL):
            self.chooseCardToReveal()
            self.chooseSanctuaryCard()
            self.chooseRegionCard()
            self.RegionCardRevealed = []
            self.nbTurns += 1

        self.displayEnd()
        
        return