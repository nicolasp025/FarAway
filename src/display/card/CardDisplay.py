import pygame
import sys

sys.path.append("./src/card/")
sys.path.append("./src/enum/")
from Card import Card
from RegionCard import RegionCard
from SanctuaryCard import SanctuaryCard
from Colors import Colors
from Stones import Stones
from Quest import Quest
from RegionQuestDisplay import RegionQuestDisplay
from SanctuaryQuestDisplay import SanctuaryQuestDisplay

## Class that displays a card
class CardDisplay():

    border_radius       = -1
    banner_Ypos_coef    = 0.6
    banner_height_coef  = 0.11
    map_size_coef       = 0.17
    stone_size_coef     = 0.15
    stone_offset_coef   = 0.05
    background_colors   = {
        Colors.GREEN : ((145, 240, 145), (35, 140, 35)), 
        Colors.RED: ((255, 100, 70), (100, 0, 0)),
        Colors.BLUE: ((135, 205, 250), (0, 0, 140)),
        Colors.YELLOW: ((255, 255, 100), (255, 215, 0)),
        Colors.GRAY: ((190, 190, 190), (130, 130, 130))
    }


    def __init__(self, card, screen, width:int, height:int):
        self.card = card
        self.screen = screen
        self.width = width
        self.height = height
        self.rect = None

        self.banner_width = width
        self.banner_height = CardDisplay.banner_height_coef * height

        if self.card.map: 
            self.map_height = self.height * CardDisplay.map_size_coef
            self.map_width = self.map_height
            
        self.stone_size = (width + height)/2 * CardDisplay.stone_size_coef
        self.stone_offset = height * CardDisplay.stone_offset_coef

        if CardDisplay.border_radius == -1:
            CardDisplay.border_radius = int(0.04 * (width + height))


    ## Display the map
    def displayMap(self, x:int, y:int) -> None:
        if self.card.map:
            img_map = pygame.image.load("./data/img/map.png")
            img_map = pygame.transform.scale(img_map, (self.map_width, self.map_height))
            self.screen.blit(img_map, self.getMapCoords(x, y))


    ## Check if the card is clicked
    def clickIn(self, coord_clic:tuple[int, int]) -> bool:
        return self.rect.collidepoint(coord_clic[0], coord_clic[1])


    ## Get the background color of the card
    def backgroundColor(self, x:int, y:int) -> tuple[tuple[int, int, int], pygame.Rect, pygame.Rect]:
        # Rectangle representing the all card
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Two rectangles representing the top and the bottom of the card
        rect1 = pygame.Rect(x, y+(self.height/3)*2, self.width, self.height/3)
        rect2 = pygame.Rect(x, y, self.width, (self.height/3)*2)

        return CardDisplay.background_colors[self.card.color], rect1, rect2


    ## Display the banner of the card
    def displayBanner(self, x:int, y:int) -> None:
        img = pygame.image.load("./data/img/"+Colors.toStringLower(self.card.color)+"_banner.png")
        img = pygame.transform.scale(img, (self.banner_width, self.banner_height))
        self.screen.blit(img, (x, y + self.height * CardDisplay.banner_Ypos_coef))


    ## Display the stones of the card
    def displayStones(self, x:int, y:int) -> None:
        images = Stones.stonesToImage(self.card.stones, self.stone_size)
        last_x = 0
        for img in images:
            self.screen.blit(img, (x+self.width-img.get_width()+last_x-self.stone_offset, y+self.stone_offset))
            last_x -= img.get_width()
    

    ## Display the card
    def display(self, x:int, y:int) -> None:
        (col1, col2), rect1, rect2 = self.backgroundColor(x, y)
        pygame.draw.rect(self.screen, col1, rect1, border_radius=CardDisplay.border_radius) 
        pygame.draw.rect(self.screen, col2, rect2, border_radius=CardDisplay.border_radius) 

        self.displayStones(x, y)

        if type(self.card) == RegionCard:
            RegionQuestDisplay(self.card.quest, self.screen, self.width, self.height).display(x, y, col1)
        else:
            SanctuaryQuestDisplay(self.card.quest, self.screen, self.width, self.height).display(x, y)

        self.displayBanner(x, y)

        # Display a border around the card
        r = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(self.screen, (255,255,255), r, 3, border_radius=CardDisplay.border_radius)
        
        self.displayMap(x, y)
        
