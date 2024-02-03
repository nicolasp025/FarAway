import sys
import json
import pygame
from random import shuffle
import time

sys.path.append("./src/player/")
sys.path.append("./src/card/")
sys.path.append("./src/enum/")
sys.path.append("./src/display/card/")
sys.path.append("./src/display/")

from Triangle import Triangle
from State import State
from Colors import Colors
from Quest import Quest
from Stones import Stones
from Player import Player
from RegionCard import RegionCard
from SanctuaryCard import SanctuaryCard
from ConditionModes import ConditionModes
from RegionCardDisplay import RegionCardDisplay
from SanctuaryCardDisplay import SanctuaryCardDisplay

class BoardDisplay:

    NBOFREGIONCARDS = 68
    NBOFSANCTUARYCARDS = 45

    WIDTHSANCTUARY = 280
    HEIGHTSANCTUARY = 400

    WIDTHREGION = 400
    HEIGHTREGION = 400
    
    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode((2160, 1440), pygame.FULLSCREEN)
        pygame.display.set_caption("Projet - Far Away")
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.nbJoueur = 2
    
        self.state = State.START
        self.RegionCardRevealed = []

        self.clic = 0

        self.players = []
        self.actualPlayer = None
        self.cpt = 0

        self.nbTurns = 0

        self.starting = []
            
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

                conditionMode = ConditionModes.castToMode(line['conditionMode'])

                tmp = []
                if conditionMode == ConditionModes.STONE:
                    for s in line['condition']:
                        tmp.append(Stones.castToStone(s))
                elif conditionMode == ConditionModes.COLOR or conditionMode == ConditionModes.SOMECOLOR:
                    for c in line['condition']:
                        tmp.append(Colors.castToColor(c))


                quest = Quest([], line['points'], conditionMode, tmp)
                
                tmpColor = Colors.castToColor(line['color'])    # Getting the color of the card
                tmpStones = []                                  # Getting the list of stones
                for s in line['stones']:
                    tmpStones.append(Stones.castToStone(s))

                card = SanctuaryCard(id, tmpColor, quest, tmpStones, eval(line['night']), eval(line['map']))

                dcard = SanctuaryCardDisplay(card, self.screen, self.WIDTHSANCTUARY, self.HEIGHTSANCTUARY)

                card.addDisplayCard(dcard)

                self.sanctuaryCards.append(card)




    def initializeRegionCards(self):
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


                quest = Quest([], line['points'], conditionMode, tmp)

                tmpColor = Colors.castToColor(line['color'])    # Getting the color of the card
                tmpStones = []                                  # Getting the list of stones
                for s in line['stones']:
                    tmpStones.append(Stones.castToStone(s))

                card = RegionCard(id, tmpColor, quest, tmpStones, eval(line['day']), eval(line['map']))

                dcard = RegionCardDisplay(card, self.screen, self.WIDTHREGION, self.HEIGHTREGION)

                card.addDisplayCard(dcard)

                self.regionCards.append(card)
        
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
                
                               
    def chooseNbPlayers(self):
        midW = self.screen.get_width()/2
        midH = self.screen.get_height()/2
        ecart = 200
        col = (255,255,255)
        points_triangle1 = [(midW+ecart, midH), (midW+ecart, midH+180), (midW+180+ecart, midH+90)]
        tr1 = Triangle(points_triangle1)
        tr1.dessiner(self.screen, col)
        points_triangle2 = [(midW-ecart, midH), (midW-ecart, midH+180), (midW-180-ecart, midH+90)]
        tr2 = Triangle(points_triangle2)
        tr2.dessiner(self.screen, col)
        
        sizeP = 400
        police = pygame.font.Font(None, sizeP)
        text_nbJ = pygame.Rect(midW-80, midH-40, 100, 50)
        
        policet = pygame.font.Font(None, 100)
        text_title = pygame.Rect(midW-500, midH-200, 400, 50)
        textt = "Choose the number of players :"

        text_val = pygame.Rect(midW-140, midH+300, 290, 70)
        textv = "Validate"

        nbJ = self.nbJoueur
        if self.clic==2:
            pos = pygame.mouse.get_pos()
            if tr1.clickIn(pos):
                nbJ = min(6, nbJ+1)
            elif tr2.clickIn(pos):
                nbJ = max(2, nbJ-1)
            elif text_val.collidepoint(pos[0], pos[1]):
                for i in range(1,self.nbJoueur+1):
                    self.players.append(Player(i))
                    for j in range(3):
                        card = self.regionCards.pop(0)
                        self.players[i-1].addCardToHand(card)
                self.actualPlayer = self.players[self.cpt]
                self.state = State.REVEAL

        self.nbJoueur = nbJ
        text = str(self.nbJoueur)
        pygame.draw.rect(self.screen, (0,0,0), text_nbJ)
        texte_surface = police.render(text, True, col)  
        self.screen.blit(texte_surface, (text_nbJ.x + 5, text_nbJ.y + 5))

        pygame.draw.rect(self.screen, (0,0,0), text_title)
        textet_surface = policet.render(textt, True, col)  
        self.screen.blit(textet_surface, (text_title.x + 5, text_title.y + 5))

        pygame.draw.rect(self.screen, col, text_val, 2)
        textev_surface = policet.render(textv, True, col)  
        self.screen.blit(textev_surface, (text_val.x + 5, text_val.y + 5))

    def next(self, state):
        self.cpt +=1
        if self.cpt < self.nbJoueur:
            self.actualPlayer = self.players[self.cpt]
            return False
        else:
            self.cpt = 0
            self.actualPlayer = self.players[self.cpt]
            self.state = state
            return True


    def chooseCardToReveal(self):
        police = pygame.font.Font(None, 120)
        text_reveal = pygame.Rect(250, self.screen.get_height()-700, 100, 50)
        textr = "Player "+str(self.actualPlayer.id)+": Choose the card you want to reveal :"
        pygame.draw.rect(self.screen, (0,0,0), text_reveal)
        texte_surface = police.render(textr, True, (255,255,255))  
        self.screen.blit(texte_surface, (text_reveal.x + 5, text_reveal.y + 5))

        i=1
        for card in self.actualPlayer.hand:
            x = i*(self.screen.get_height()/3)-70
            y = self.screen.get_height()-500
            card.dcard.display(x, y)
            pos = pygame.mouse.get_pos()
            if card.dcard.clickIn(pos):
                r = pygame.Rect(x, y, self.WIDTHREGION, self.HEIGHTREGION)
                pygame.draw.rect(self.screen, (255,255,255), r, 7, border_radius=30)
                if self.clic==2:
                    n = self.actualPlayer.revealCard(i)
                    self.starting.append((self.actualPlayer, n))
                    if self.next(State.SANCTUARY):
                        self.starting.sort(key=lambda x : x[1])
                        self.players = [t[0] for t in self.starting]
            i+=1
            

    def chooseSanctuaryCard(self):
        police = pygame.font.Font(None, 120)
        text_sanc = pygame.Rect(250, self.screen.get_height()-700, 100, 50)
        textr = "Player "+str(self.actualPlayer.id)+": Choose the sanctuary card you want :"
        pygame.draw.rect(self.screen, (0,0,0), text_sanc)
        texte_surface = police.render(textr, True, (255,255,255))  
        self.screen.blit(texte_surface, (text_sanc.x + 5, text_sanc.y + 5))
    
        nbToAdd = self.actualPlayer.sanctuaryCardToAdd() 

        if nbToAdd > 0:
            for i in range(nbToAdd):
                card = self.sanctuaryCards[i]
                x = (i+1)*(300)-70
                y = self.screen.get_height()-500
                card.dcard.display(x, y)
                pos = pygame.mouse.get_pos()
                if card.dcard.clickIn(pos):
                    r = pygame.Rect(x, y, self.WIDTHSANCTUARY, self.HEIGHTSANCTUARY)
                    pygame.draw.rect(self.screen, (255,255,255), r, 7, border_radius=30)
                    if self.clic==2:
                        self.actualPlayer.addCardToSanctuaryCards(self.sanctuaryCards.pop(i))
                        for j in range(nbToAdd-1):
                            self.sanctuaryCards.pop(i)
                        self.next(State.REGION)
                        
        else:
            self.cpt+=1
            if self.cpt < self.nbJoueur:
                self.actualPlayer = self.players[self.cpt]
            else:
                self.cpt = 0
                self.actualPlayer = self.players[self.cpt]
                self.state = State.REGION



            
    def chooseRegionCard(self):
        police = pygame.font.Font(None, 120)
        text_reg = pygame.Rect(260, self.screen.get_height()-700, 100, 50)
        textr = "Player "+str(self.actualPlayer.id)+": Choose the region card you want :"
        pygame.draw.rect(self.screen, (0,0,0), text_reg)
        texte_surface = police.render(textr, True, (255,255,255))  
        self.screen.blit(texte_surface, (text_reg.x + 5, text_reg.y + 5))

        for i in range(self.nbJoueur+1-self.cpt):
            card = self.regionCards[i]
            x = (i+1)*(self.screen.get_height()/3)-70
            y = self.screen.get_height()-500
            card.dcard.display(x, y)
            pos = pygame.mouse.get_pos()
            if card.dcard.clickIn(pos):
                r = pygame.Rect(x, y, self.WIDTHREGION, self.HEIGHTREGION)
                pygame.draw.rect(self.screen, (255,255,255), r, 7, border_radius=30)
                if self.clic==2:
                    self.actualPlayer.addCardToHand(self.regionCards.pop(i))

                    if self.next(State.REVEAL):
                        self.nbTurns += 1
                        self.regionCards.pop(0)
                    break


    def displayEnd(self):
        police = pygame.font.Font(None, 120)
        text_end = pygame.Rect(self.screen.get_width()/2-300, self.screen.get_height()-700, 100, 50)
        textr = "Game is finished !"
        pygame.draw.rect(self.screen, (0,0,0), text_end)
        texte_surface = police.render(textr, True, (255,255,255))  
        self.screen.blit(texte_surface, (text_end.x + 5, text_end.y + 5))

    def execute(self):
        if self.nbTurns == 8:
            self.state = State.END
        if self.state == State.START:
            self.chooseNbPlayers()
        elif self.state == State.REVEAL:
            self.chooseCardToReveal()
        elif self.state == State.SANCTUARY:
            self.chooseSanctuaryCard()
        elif self.state == State.REGION:
            self.chooseRegionCard()
        elif self.state == State.END:
            self.displayEnd()

    def play(self):

        while self.running :

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Vérifier si le bouton de la souris est enfoncé
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.clic = 1

                # Vérifier si le bouton de la souris est relâché
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clic == 1:
                    self.clic = 2

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("black")

            self.execute()
            
            if self.clic == 2:
                self.clic = 0
            # flip() the display to put your work on screen
            pygame.display.flip()

            dt = self.clock.tick(60) / 1000

        pygame.quit()
        
        return