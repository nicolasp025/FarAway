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

class CardDisplay():

    def __init__(self, card, screen, width, height):
        self.card = card
        self.screen = screen
        self.width = width
        self.height = height
        self.rect = None

    def getMapCoords(self, x, y):
        return (x+self.width*0.25, y+10)

    def displayMap(self, x, y):
        if self.card.map:
            img_map = pygame.image.load("./data/img/map.png")
            img_map = pygame.transform.scale(img_map, (70, 70))
            self.screen.blit(img_map, self.getMapCoords(x, y))


    def questDisplay(self):
        if type(self.card) == RegionCard:
            return RegionQuestDisplay(self.card.quest, self.screen, self.width, self.height)
        return SanctuaryQuestDisplay(self.card.quest, self.screen, self.width, self.height)


    def clickIn(self, coord_clic):
        return self.rect.collidepoint(coord_clic[0], coord_clic[1])

    def backgroundColor(self, x, y):
        self.rect = pygame.Rect(x, y, self.width, self.height)
        rect1 = pygame.Rect(x, y+(self.height/3)*2, self.width, self.height/3)
        rect2 = pygame.Rect(x, y, self.width, (self.height/3)*2)
        colors = None, None
        if self.card.color == Colors.GREEN:
            colors =  (144, 238, 144), (34, 139, 34)
        elif self.card.color == Colors.RED:
            colors =  (255, 100, 70), (100, 0, 0)
        elif self.card.color ==  Colors.BLUE:
            colors =  (135, 206, 250), (0, 0, 139)
        elif self.card.color == Colors.YELLOW:
            colors =  (255, 255, 102), (255, 215, 0)
        elif self.card.color == Colors.GRAY:
            colors = (192, 192, 192), (128, 128, 128)
        return colors, rect1, rect2
        
    def displayBanner(self, x, y):
        img = pygame.image.load("./data/img/"+Colors.toStringLower(self.card.color)+"_banner.png")
        img = pygame.transform.scale(img, (self.width, 35))
        self.screen.blit(img, (x, y+(self.height/3)*2-15))

    def displayStones(self, x, y):
        images = Stones.stonesToImage(self.card.stones)
        last_x = 0
        for img in images:
            self.screen.blit(img, (x+self.width-img.get_width()+last_x-10, y+10))
            last_x -= img.get_width()
    
    def display(self, x, y):
        (col1, col2), rect1, rect2 = self.backgroundColor(x, y)
        pygame.draw.rect(self.screen, col1, rect1, border_radius=30) 
        pygame.draw.rect(self.screen, col2, rect2, border_radius=30) 

        self.displayStones(x, y)
        self.displayBanner(x, y)
        r = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(self.screen, (255,255,255), r, 3, border_radius=30)
        self.displayMap(x, y)
        self.questDisplay().display(x, y, col1)