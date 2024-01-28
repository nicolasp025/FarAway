import pygame
import sys

sys.path.append("./src/card/")
sys.path.append("./src/enum/")
from SanctuaryCard import SanctuaryCard
from Colors import Colors
from Stones import Stones
from Quest import Quest
from CardDisplay import CardDisplay

class SanctuaryCardDisplay(CardDisplay):

    def __init__(self, card, screen, width, height):
        super().__init__(card, screen, width, height)

    def dayDisplay(self, night):
        img_day = None
        if night:
            img_day = pygame.image.load("./data/img/night.png")
            img_day = pygame.transform.scale(img_day, (70, 70))
            self.screen.blit(img_day, (self.x+10,self.y+10))
        return img_day


    # def questDisplay(self, quest):



    def sanctuaryCardDisplay(self, x, y):
        super().display(x, y)
        
        dec = 0
        img_day = self.dayDisplay(self.card.day)
        if  img_day != None:
            dec = img_day.get_width()
