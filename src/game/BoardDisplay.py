import sys
import json
import pygame
from random import shuffle
import time

sys.path.append("./src/player/")
sys.path.append("./src/card/")
sys.path.append("./src/enum/")
sys.path.append("./src/display/card/")

from Colors import Colors
from Quest import Quest
from Stones import Stones
from Player import Player
from RegionCard import RegionCard
from SanctuaryCard import SanctuaryCard
from ConditionModes import ConditionModes
from RegionCardDisplay import RegionCardDisplay

class BoardDisplay:

    NBOFREGIONCARDS = 68
    NBOFSANCTUARYCARDS = 45
    
    def __init__(self, players):
        
        pygame.init()
        self.screen = pygame.display.set_mode((1980, 1280))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
    

        self.RegionCardsToDisplay = []
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
        with open("./data/SanctuaryCards.json") as f:
            data = json.load(f)
            i = 0
            for line in data['sanctuaryCards']:
                i += 1
                id = str(line['id']).replace("sanctuary-", "")
                quest = Quest([], line['points'], ConditionModes.castToMode(line['conditionMode']), line['condition'])
                
                tmpColor = Colors.castToColor(line['color'])    # Getting the color of the card
                tmpStones = []                                  # Getting the list of stones
                for s in line['stones']:
                    tmpStones.append(Stones.castToStone(s))
                
                self.sanctuaryCards.append(SanctuaryCard(id, tmpColor, quest, tmpStones, eval(line['night']), eval(line['map'])))
            print(str(i) + " sanctuary cards has been successfully generated.")


    def initializeRegionCards(self):
        with open("./data/RegionCards.json") as f:
            data = json.load(f)
            i = 0
            for line in data['regionCards']:
                i += 1
                id = str(line['id']).replace("region-", "")
                quest = Quest(line['require'], line['points'], ConditionModes.castToMode(line['conditionMode']), line['condition'])

                tmpColor = Colors.castToColor(line['color'])    # Getting the color of the card
                tmpStones = []                                  # Getting the list of stones
                for s in line['stones']:
                    tmpStones.append(Stones.castToStone(s))

                self.regionCards.append(RegionCard(id, tmpColor, quest, tmpStones, eval(line['day']), eval(line['map'])))
            print(str(i) + " region cards has been successfully generated.")
        
    def reverseList(x):
        res = []
        for i in x:
            res.append(i)
        return res

    def countFinalPoints():
        res = {} 
        for p in self.players:
            tmpScore = 0

            ressources = {"map" : 0, "night": 0, "day": 0}
            # Getting all bonuses from sanctuaryCards
            for card in p.sanctuaryCards:

                ## Adding the color of the sanctuary card
                if card.color not in ressources:
                    ressources[card.color] = 1
                else:
                    ressources[card.color] += 1
                
                ## Adding the stones of the sanctuary card
                for stone in card.stones:
                    if stone not in ressources:
                        ressources[stone] = 1
                    else:
                        ressources[stone] += 1
                
                ## Adding the map
                if card.map:
                    ressources["map"] += 1
                
                ## Adding the night
                if card.night:
                    ressources["night"] += 1
                else:
                    ressources["day"] += 1

            # Getting points from every region card
            for card in reverse(p.revealedCards):
                if card.satisfy(ressources):
                    pass
                    # to continue
                

                



















    def play(self):
        print("----------------- Start of the Game ------------------- \n\n")
        ## Setup of the game 
        for i in range(len(self.players)):
            for j in range(3):
                card = self.regionCards.pop(0)
                self.players[i].addCardToHand(card)
                self.RegionCardsToDisplay.append(RegionCardDisplay(card, self.screen, self.clock, j*500+100, self.screen.get_height()-500-i*500, 400, 400))

        while self.running :


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("black")
            
            nbTurns = 0

            for card in self.RegionCardsToDisplay:
                card.regionCardDisplay()


            # ### Choose the card to reveal
            # while(nbTurns < Player.NBCARDSTOREVEAL and self.running):
            #     print("----------------- Turn number "+str(nbTurns+1)+" -----------------\n")
            #     for i in range(len(self.players)+1):
            #         self.RegionCardRevealed.append(self.regionCards.pop(0))

            #     print("----------------- Choose the card you want to reveal ------------------- \n")
            #     starting = []
            #     for p in self.players:
            #         index = -1
            #         while(type(index) != int or index <= 0 or index > Player.NBCARDSINHAND):
            #             i=1
            #             print("Player "+str(p.id)+" cards :")
            #             for card in p.hand:
            #                 print(str(i)+" : "+card.toString())
            #                 i+=1
            #             inp = input("Player "+str(p.id)+" : Enter the index of the card you want to reveal : ")
            #             if str.isdigit(inp):
            #                 index = int(inp)
            #         n = p.revealCard(int(index))
            #         starting.append((p, n))
            #         print("Player "+str(p.id)+" has revealed "+p.revealedCards[-1].toString()+"\n")
            #         print("\n")


            #     print("----------------- Choose the sanctuary card you want to add to your hand  ------------------- \n")
            #     ## Choose sanctuary card if you had to
            #     for p in self.players:
            #         nbToAdd = p.sanctuaryCardToAdd()
            #         if nbToAdd > 0:
            #             print("Player "+str(p.id)+" sanctuary cards available :")
            #             index = -1
            #             while(type(index) != int or index <= 0 or index > nbToAdd):
            #                 for i in range(1, nbToAdd+1):
            #                     print(str(i)+" : "+self.sanctuaryCards[i-1].toString())
            #                 inp = input("Player "+str(p.id)+" : Enter the index of the sanctuary card you want to take : ")
            #                 if str.isdigit(inp):
            #                     index = int(inp)
            #             p.addCardToSanctuaryCards(self.sanctuaryCards.pop(index-1))
            #             for i in range(nbToAdd-1):
            #                 self.sanctuaryCards.pop(0)
            #             print("Player "+str(p.id)+" has taken "+p.sanctuaryCards[-1].toString()+"\n")
            #             print("\n")


            #     ## Set the new list of player with the right order 
            #     starting.sort(key=lambda x : x[1])
            #     self.players = [t[0] for t in starting]

            #     if (nbTurns < 7):
            #         print("----------------- Choose the region card you want to add to your hand  ------------------- \n")
            #         ## Choose the region card for player hand
            #         for p in self.players:
            #             index = -1
            #             while(type(index) != int or index <= 0 or index > len(self.players)+2):
            #                 i=1
            #                 print("All cards available :\n")
            #                 for card in self.RegionCardRevealed:
            #                     print(str(i)+" : "+card.toString())
            #                     i+=1
            #                 inp = input("Player "+str(p.id)+" : Enter the index of the card you want to choose: ")
            #                 if str.isdigit(inp):
            #                     index = int(inp)
            #             card = self.RegionCardRevealed.pop(index-1)
            #             p.addCardToHand(card)
            #             print("Player "+str(p.id)+" has choose "+card.toString()+"\n")
            #             print("\n")

            #     self.RegionCardRevealed = []
            #     nbTurns += 1



            # print("----------------- Final Cards for each player  ------------------- \n")
            # ## Print final cards revealed by players
            # for p in self.players:
            #     print("Player "+str(p.id)+" final cards :")
            #     for c in p.revealedCards:
            #         print(c.toString())
                    
            # print("------------ Counting points ------------")
            # print(countFinalPoints())

            # print("Game end\n")

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = self.clock.tick(60) / 1000

        pygame.quit()
        
        return