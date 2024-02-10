import sys
import json
from random import shuffle

sys.path.append("./src/player/")
sys.path.append("./src/card/")
sys.path.append("./src/enum/")
sys.path.append("./src/display/card/")
sys.path.append("./src/display/")

from Colors import Colors
from Quest import Quest
from Stones import Stones
from Player import Player
from RegionCard import RegionCard
from SanctuaryCard import SanctuaryCard
from ConditionModes import ConditionModes
from RegionCardDisplay import RegionCardDisplay
from SanctuaryCardDisplay import SanctuaryCardDisplay

class Board:

    NBOFSANCTUARYCARDS = 45
    WIDTHSANCTUARY = 280
    HEIGHTSANCTUARY = 400

    NBOFREGIONCARDS = 68
    WIDTHREGION = 400
    HEIGHTREGION = 400

    MINIMUMPLAYERS = 2
    MAXIMUMPLAYERS = 6


    def __init__(self, screen=None):

        self.RegionCardRevealed = []
        self.players = []
        self.nbTurns = 0
            
        # Initializing the region cards
        self.regionCards = []
        self.initializeRegionCards(screen)
        shuffle(self.regionCards)

        # Initializing the sanctuary cards
        self.sanctuaryCards = []
        self.initializeSanctuaryCards(screen)
        shuffle(self.sanctuaryCards)


    def initializeSanctuaryCards(self, screen=None):
        with open("./data/SanctuaryCards.json") as f:
            data = json.load(f)
            i = 0
            for line in data['sanctuaryCards']:
                i += 1
                id = str(line['id']).replace("sanctuary-", "")
                conditionMode = ConditionModes.castToMode(line['conditionMode'])
                tmp = []
                if conditionMode == ConditionModes.STONE:
                    for s in line['condition']:
                        tmp.append(Stones.castToStone(s))
                elif conditionMode == ConditionModes.COLOR or conditionMode == ConditionModes.SOMECOLOR:
                    for c in line['condition']:
                        tmp.append(Colors.castToColor(c))
                quest = Quest([], eval(line['points']), conditionMode, tmp)
                tmpColor = Colors.castToColor(line['color'])    # Getting the color of the card
                tmpStones = []                                  # Getting the list of stones
                for s in line['stones']:
                    tmpStones.append(Stones.castToStone(s))

                card = SanctuaryCard(id, tmpColor, quest, tmpStones, eval(line['night']), eval(line['map']))
                if screen != None:
                    dcard = SanctuaryCardDisplay(card, screen, self.WIDTHSANCTUARY, self.HEIGHTSANCTUARY)
                    card.addDisplayCard(dcard)
                self.sanctuaryCards.append(card)


    def initializeRegionCards(self, screen=None):
        with open("./data/RegionCards.json") as f:
            data = json.load(f)
            i = 0
            for line in data['regionCards']:
                i += 1
                id = str(line['id']).replace("region-", "")
                conditionMode = ConditionModes.castToMode(line['conditionMode'])
                tmp = []
                if conditionMode == ConditionModes.STONE:
                    for s in line['condition']:
                        tmp.append(Stones.castToStone(s))
                elif conditionMode == ConditionModes.COLOR or conditionMode == ConditionModes.SOMECOLOR:
                    for c in line['condition']:
                        tmp.append(Colors.castToColor(c))
                tmpReq = []
                for s in line['require']:
                    tmpReq.append(Stones.castToStone(s))
                quest = Quest(tmpReq, eval(line['points']), conditionMode, tmp)
                tmpColor = Colors.castToColor(line['color'])    # Getting the color of the card
                tmpStones = []                                  # Getting the list of stones
                for s in line['stones']:
                    tmpStones.append(Stones.castToStone(s))

                card = RegionCard(id, tmpColor, quest, tmpStones, eval(line['day']), eval(line['map']))
                if screen != None:
                    dcard = RegionCardDisplay(card, screen, self.WIDTHREGION, self.HEIGHTREGION)
                    card.addDisplayCard(dcard)
                self.regionCards.append(card)


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
            for card in p.revealedCards[::-1]:
                ressources = self.addRessources(ressources, card)
                tmpScore += card.satisfy(ressources)

            res[p.id] = tmpScore
        return res