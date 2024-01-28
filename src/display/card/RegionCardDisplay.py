import pygame
import sys

sys.path.append("./src/card/")
sys.path.append("./src/enum/")
from RegionCard import RegionCard
from Colors import Colors
from Stones import Stones
from Quest import Quest
from CardDisplay import CardDisplay

class RegionCardDisplay(CardDisplay):

    def __init__(self, card, screen, width, height):
        super().__init__(card, screen, width, height)


    def dayDisplay(self, day):
        img_day = None
        if day:
            img_day = pygame.image.load("./data/img/day.png")
        else:
            img_day = pygame.image.load("./data/img/night.png")
        img_day = pygame.transform.scale(img_day, (70, 70))
        return img_day

    def idDisplay(self, id):
        police = pygame.font.Font(None, 40)  
        texte = str(id)
        surface_texte = police.render(texte, True, (0, 0, 0))
        return surface_texte

    # def questDisplay(self, quest):


    def display(self, x, y):
        super().display(x, y)

        img_day = self.dayDisplay(self.card.day)
        self.screen.blit(img_day, (x+10,y+10))

        self.screen.blit(self.idDisplay(self.card.id), (x+img_day.get_width()/2, y+img_day.get_height()/2-2))

