import pygame
import sys

sys.path.append("./src/card/")
sys.path.append("./src/enum/")
from SanctuaryCard import SanctuaryCard
from Colors import Colors
from Stones import Stones
from Quest import Quest
from CardDisplay import CardDisplay

## The class which represent the display of the sanctuary card
class SanctuaryCardDisplay(CardDisplay):

    night_width_coef        = 0.33
    night_height_coef       = 0.21
    night_pos_coef          = 0.015
    map_night_posX_coef     = 0.35
    map_day_posX_coef       = 0.06
    map_posY_coef           = 0.04


    def __init__(self, card, screen, width:int, height:int):
        super().__init__(card, screen, width, height)

        self.night_width = width * SanctuaryCardDisplay.night_width_coef
        self.night_height = height * SanctuaryCardDisplay.night_height_coef
        self.night_posX = width * SanctuaryCardDisplay.night_pos_coef
        self.night_posY = height * SanctuaryCardDisplay.night_pos_coef

        if not self.card.day:
            self.map_posX = SanctuaryCardDisplay.map_night_posX_coef * width
        else :
            self.map_posX = SanctuaryCardDisplay.map_day_posX_coef * width
        self.map_posY = SanctuaryCardDisplay.map_posY_coef * height


    ## Display the night icon
    def displayNight(self, x:int, y:int) -> None:
        if not self.card.day: 
            img_day = pygame.image.load("./data/img/night.png")
            img_day = pygame.transform.scale(img_day, (self.night_width, self.night_height))
            self.screen.blit(img_day, (x + self.night_posX, y + self.night_posY))

    ## Get the coordinate of the map image
    def getMapCoords(self, x:int, y:int) -> tuple[int, int]:
        return (x+self.map_posX, y+self.map_posY)


    ## Display the sanctuary card
    def display(self, x, y):
        super().display(x, y)     
        self.displayNight(x, y)
