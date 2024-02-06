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

from Board import Board
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
from ChooseNbPlayer import ChooseNbPlayer

class BoardDisplay(Board):
    
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((2160, 1440), pygame.FULLSCREEN)
        pygame.display.set_caption("Projet - Far Away")
        self.clock = pygame.time.Clock()
        super().__init__(self.screen)

        self.running = True

        self.nbJoueur = 2
    
        self.state = State.START

        self.clic = 0

        self.players = []
        self.actualPlayer = None
        self.cpt = 0

        self.nbTurns = 0

        self.starting = []

    def chooseNbPlayers(self):
        nbJ = ChooseNbPlayer(self.screen, super().MAXIMUMPLAYERS, super().MINIMUMPLAYERS).display(self.nbJoueur, self.clic)
        self.nbJoueur = nbJ[1]
        if nbJ[0]:
            for i in range(1,self.nbJoueur+1):
                self.players.append(Player(i))
                for j in range(3):
                    card = self.regionCards.pop(0)
                    self.players[i-1].addCardToHand(card)
            self.actualPlayer = self.players[self.cpt]
            self.state = State.REVEAL


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