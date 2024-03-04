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

    def __init__(self, card, screen, width:int, height:int):
        super().__init__(card, screen, width, height)


    ## Display the day or night
    def dayDisplay(self) -> pygame.Surface:
        img_day = None
        if self.card.day:
            img_day = pygame.image.load("./data/img/day.png")
        else:
            img_day = pygame.image.load("./data/img/night.png")
        img_day = pygame.transform.scale(img_day, (70, 70))
        return img_day


    ## Display the id of the card
    def idDisplay(self) -> pygame.Surface:
        police = pygame.font.Font(None, 40)  
        texte = str(self.card.id)
        surface_texte = police.render(texte, True, (0, 0, 0))
        return surface_texte


    ## Display the card
    def display(self, x:int, y:int) -> None:
        super().display(x, y)


        img_day = self.dayDisplay()
        self.screen.blit(img_day, (x+10,y+10))
        
        width = img_day.get_width()
        height = img_day.get_height()

        # Display the id in the center of the img_day
        if self.card.day:
            if int(self.card.id)<10:
                self.screen.blit(self.idDisplay(), (x+width/2+4, y+height/2-3))
            else:
                self.screen.blit(self.idDisplay(), (x+width/2-3, y+height/2-3))
        else:
            if int(self.card.id)<10:
                self.screen.blit(self.idDisplay(), (x+width/2-6, y+height/2-2))
            else:
                self.screen.blit(self.idDisplay(), (x+width/2-6, y+height/2-2))

