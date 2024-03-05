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

## The class which represents the board of the game
class Board:

    NBOFSANCTUARYCARDS = 45
    WIDTHSANCTUARY = 220
    HEIGHTSANCTUARY = 350

    NBOFREGIONCARDS = 68
    WIDTHREGION = 350
    HEIGHTREGION = 350

    MINIMUMPLAYERS = 2
    MAXIMUMPLAYERS = 6


    def __init__(self, screen=None):

        self.sanctuaryCardsUsed = []
        self.RegionCardRevealed = []
        self.players = []
        self.nbTurns = 0
            
        # Initializing the region cards
        self.regionCards = []
        self.initializeCards("RegionCards.json", 1, screen)
        shuffle(self.regionCards)

        # Initializing the sanctuary cards
        self.sanctuaryCards = []
        self.initializeCards("SanctuaryCards.json", 0, screen)
        shuffle(self.sanctuaryCards)
    
    def initializeCards(self, file:str, type:int, screen=None) -> None:
        with open("./data/"+file) as f:
            data = json.load(f)

            # Load the json depending of the type
            d = {}
            if type == 0:
                d = data['sanctuaryCards']
            else:
                d = data['regionCards']

            # Create a card
            for line in d:
                id = line['id']                                                   # Getting the id of the card
                conditionMode = ConditionModes.castToMode(line['conditionMode'])  # Getting the condition mode of the card
                tmp = []
                if conditionMode == ConditionModes.STONE:
                    # The quest is about stone
                    for s in line['condition']:
                        tmp.append(Stones.castToStone(s))
                elif conditionMode == ConditionModes.COLOR or conditionMode == ConditionModes.SOMECOLOR:
                    # The quest is about colors
                    for c in line['condition']:
                        tmp.append(Colors.castToColor(c))

                require = []
                if type == 1:
                    # Getting the list of requirements
                    for s in line['require']:
                        require.append(Stones.castToStone(s))

                # Create the quest
                quest = Quest(require, eval(line['points']), conditionMode, tmp)
                tmpColor = Colors.castToColor(line['color'])    # Getting the color of the card
                tmpStones = [] 

                # Getting the list of stones                                 
                for s in line['stones']:
                    tmpStones.append(Stones.castToStone(s))

                card = None
                
                # Create the card and add it to the right stack
                if type == 0:
                    card = SanctuaryCard(id, tmpColor, quest, tmpStones, eval(line['night']), eval(line['map']))
                    self.sanctuaryCards.append(card)
                else:
                    card = RegionCard(id, tmpColor, quest, tmpStones, eval(line['day']), eval(line['map']))
                    self.regionCards.append(card)

                # If it display mode, create a display card
                if screen != None:
                    if type == 0:
                        dcard = SanctuaryCardDisplay(card, screen, self.WIDTHSANCTUARY, self.HEIGHTSANCTUARY)
                    else:
                        dcard = RegionCardDisplay(card, screen, self.WIDTHREGION, self.HEIGHTREGION)
                    card.addDisplayCard(dcard)

    ## Check if there is enough sanctuary cards in the stack
    def checkSanctuaryCards(self, nbToDraw:int) -> None:
        if nbToDraw > len(self.sanctuaryCards):
            # If not, we shuffle the used cards and add them to the stack
            self.sanctuaryCards = self.sanctuaryCardsUsed + self.sanctuaryCards
            shuffle(self.sanctuaryCards)

    ## Add ressources for the card
    def addRessources(self, ressources:dict, card) -> dict:

        # Adding the color of the card
        if card.color not in ressources:
            ressources[card.color] = 1
        else:
            ressources[card.color] += 1
    
        # Adding the stones of the card
        for stone in card.stones:
            if stone not in ressources:
                ressources[stone] = 1
            else:
                ressources[stone] += 1
        
        # Adding the map
        if card.map:
            ressources["map"] += 1
        
        # Adding the night
        if card.day:
            ressources["day"] += 1
        else:
            ressources["night"] += 1
        return ressources

    ## Get the final points of the players
    def countFinalPoints(self) -> int:
        res = {} 
        for p in self.players:
            tmpScore = 0

            # Init the ressources
            ressources = {"map" : 0, "night": 0, "day": 0}

            # Add sanctuaryCards to ressources
            for card in p.sanctuaryCards:
                ressources = self.addRessources(ressources, card)

            # Getting points from every region card (from the last to the first)
            for card in p.revealedCards[::-1]:
                ressources = self.addRessources(ressources, card)
                tmpScore += card.satisfy(ressources)

            # Getting all bonuses from sanctuaryCards
            for card in p.sanctuaryCards:
                tmpScore += card.satisfy(ressources)

            res[p.id] = tmpScore
        return res
    

    ## Choose the number of players
    def chooseNbPlayers(self) -> None:
        pass

    ## Choose the card to reveal
    def chooseCardToReveal(self) -> None:
        pass

    ## Choose the sanctuary card
    def chooseSanctuaryCard(self) -> None:
        pass

    ## Choose the region card
    def chooseRegionCard(self) -> None:
        pass

    ## Display the end of the game
    def displayEnd(self) -> None:
        pass