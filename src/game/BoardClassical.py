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

        # Getting the number of players
        print("How many players do you want to play with ?")
        nbPlayers = int(input("Number of players should be between "+ str(super().MINIMUMPLAYERS) + " and " + str(super().MAXIMUMPLAYERS) + " : "))
        
        if nbPlayers < super().MINIMUMPLAYERS or nbPlayers > super().MAXIMUMPLAYERS:
            print("Error: the specified number of players is incorrect, please restart.")
            return
        
        # Generate all the players
        self.players = []
        for i in range(nbPlayers):
            self.players.append(Player(i))
        print("The " + str(nbPlayers) + " players has been successfully created.")
    
    def reverseList(self, x):
        res = []
        for i in x:
            res.append(i)
        return res

    def addRessources(self, ressources, card):

         ## Adding the color of the card
        if card.color not in ressources:
            ressources[card.color] = 1
        else:
            ressources[card.color] += 1
    
        ## Adding the stones of the card
        for stone in card.stones:
            if stone not in ressources:
                ressources[stone] = 1
            else:
                ressources[stone] += 1
        
        ## Adding the map
        if card.map:
            ressources["map"] += 1
        
        ## Adding the night
        if card.day:
            ressources["day"] += 1
        else:
            ressources["night"] += 1
        return ressources

    def countFinalPoints(self):
        res = {} 
        for p in self.players:
            tmpScore = 0

            ressources = {"map" : 0, "night": 0, "day": 0}
            # Getting all bonuses from sanctuaryCards
            for card in p.sanctuaryCards:
                ressources = self.addRessources(ressources, card)

            # Getting points from every region card
            for card in self.reverseList(p.revealedCards):
                ressources = self.addRessources(ressources, card)
                tmpScore += card.satisfy(ressources)

            res[p.id] = tmpScore
        return res
                

    def play(self):
        nbTurns = 0
        print("----------------- Start of the Game ------------------- \n\n")
        ## Setup of the game 
        for i in range(len(self.players)):
            for j in range(3):
                self.players[i].addCardToHand(self.regionCards.pop(0))

        ### Choose the card to reveal
        while(nbTurns < Player.NBCARDSTOREVEAL):
            print("----------------- Turn number "+str(nbTurns+1)+" -----------------\n")
            for i in range(len(self.players)+1):
                self.RegionCardRevealed.append(self.regionCards.pop(0))

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


            print("----------------- Choose the sanctuary card you want to add to your hand  ------------------- \n")
            ## Choose sanctuary card if you had to
            for p in self.players:
                nbToAdd = p.sanctuaryCardToAdd()
                if nbToAdd > 0:
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
                        self.sanctuaryCards.pop(0)
                    print("Player "+str(p.id)+" has taken "+p.sanctuaryCards[-1].toString()+"\n")
                    print("\n")


            ## Set the new list of player with the right order 
            starting.sort(key=lambda x : x[1])
            self.players = [t[0] for t in starting]

            if (nbTurns < 7):
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

            self.RegionCardRevealed = []
            nbTurns += 1



        print("----------------- Final Cards for each player  ------------------- \n")
        ## Print final cards revealed by players
        for p in self.players:
            print("Player "+str(p.id)+" final cards :")
            for c in p.revealedCards:
                print(c.toString())
                
        print("------------ Counting points ------------")
        print(self.countFinalPoints())

        print("Game end\n")
        
        return