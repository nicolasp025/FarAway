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
        self.iconSize = 70

    def displayNight(self, x, y):
        if self.card.day:
            img_day = pygame.image.load("./data/img/night.png") # don't mind the logic
            img_day = pygame.transform.scale(img_day, (self.iconSize, self.iconSize))
            self.screen.blit(img_day, (x+10, y+5))

    def getMapCoords(self, x, y):
        if self.card.day:
            return (x+self.iconSize+10, y+5)
        return (x+10, y+5)

    def display(self, x, y):
        super().display(x, y)     
        self.displayNight(x, y)
