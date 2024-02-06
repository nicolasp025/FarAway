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


    def dayDisplay(self):
        img_day = None
        if self.card.day:
            img_day = pygame.image.load("./data/img/day.png")
        else:
            img_day = pygame.image.load("./data/img/night.png")
        img_day = pygame.transform.scale(img_day, (70, 70))
        return img_day

    def idDisplay(self):
        police = pygame.font.Font(None, 40)  
        texte = str(self.card.id)
        surface_texte = police.render(texte, True, (0, 0, 0))
        return surface_texte



    def display(self, x, y):
        super().display(x, y)

        img_day = self.dayDisplay()
        self.screen.blit(img_day, (x+10,y+10))

        self.screen.blit(self.idDisplay(), (x+img_day.get_width()/2, y+img_day.get_height()/2-2))

