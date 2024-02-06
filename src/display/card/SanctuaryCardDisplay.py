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

    def dayDisplay(self):
        img_day = None
        if self.card.day:
            img_day = pygame.image.load("./data/img/night.png")
            img_day = pygame.transform.scale(img_day, (70, 70))
        return img_day



    def display(self, x, y):
        super().display(x, y)
        
        img_day = self.dayDisplay()
        if  img_day != None:
            img_day.blit(self.screen, (x+self.width/3, y+10))
