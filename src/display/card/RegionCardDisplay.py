import pygame
import sys

sys.path.append("./src/card/")
sys.path.append("./src/enum/")
from RegionCard import RegionCard
from Colors import Colors
from Stones import Stones
from Quest import Quest
from CardDisplay import CardDisplay

## The class to represent the display of a region card
class RegionCardDisplay(CardDisplay):

    day_pos_coef        = 0.02
    day_size_coef       = 0.3
    id_font_size_coef   = 0.56

    def __init__(self, card, screen, width:int, height:int):
        super().__init__(card, screen, width, height)

        self.day_posX = width * RegionCardDisplay.day_pos_coef
        self.day_posY = height * RegionCardDisplay.day_pos_coef
        self.day_width = self.width * RegionCardDisplay.day_size_coef
        self.day_height = self.height * RegionCardDisplay.day_size_coef

        self.idFontSize = int((self.day_height + self.day_width)/2 * RegionCardDisplay.id_font_size_coef)
        
        if int(card.id) < 10:
            self.id_posX_coef = 0.5
        else:
            self.id_posX_coef = 0.36
        self.id_posY_coef = 0.4
        self.id_posX = self.day_width * self.id_posX_coef
        self.id_posY = self.day_height * self.id_posY_coef
        


    ## Display the day or night
    def dayDisplay(self, x:int, y:int):
        img_day = None
        if self.card.day:
            img_day = pygame.image.load("./data/img/day.png")
        else:
            img_day = pygame.image.load("./data/img/night.png")
        tmpSize = (self.day_width, self.day_height)
        img_day = pygame.transform.scale(img_day, tmpSize)
        self.screen.blit(img_day, (x+self.day_posX,y+self.day_posY))


    ## Display the id of the card
    def idDisplay(self, x:int, y:int):
        police = pygame.font.Font(None, self.idFontSize)  
        texte = str(self.card.id)
        surface_texte = police.render(texte, True, (0, 0, 0))
        self.screen.blit(surface_texte, (x+self.id_posX, y+self.id_posY))


    ## Display the card
    def display(self, x:int, y:int) -> None:
        super().display(x, y)
        self.dayDisplay(x, y)   
        self.idDisplay(x, y)

