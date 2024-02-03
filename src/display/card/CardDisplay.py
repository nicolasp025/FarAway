import pygame
import sys

sys.path.append("./src/card/")
sys.path.append("./src/enum/")
from Card import Card
from Colors import Colors
from Stones import Stones
from Quest import Quest
from QuestDisplay import QuestDisplay

class CardDisplay():

    def __init__(self, card, screen, width, height):
        self.size = (width, height)
        self.card = card
        self.screen = screen
        self.width = width
        self.height = height
        self.rect = None

    def colorToColor(self, col):
        if col == Colors.GREEN:
            return "green"
        elif col == Colors.RED:
            return "red"
        elif col == Colors.BLUE:
            return "blue"
        elif col == Colors.YELLOW:
            return "yellow"
        else:
            return "gray"
        
    def stoneToImage(self, stones):
        images = []
        size = (60, 60)
        for s in stones:
            if s == Stones.EMERALD:
                img = pygame.image.load("./data/img/emerald.png")
                img = pygame.transform.scale(img, size)
                images.append(img)
            elif s == Stones.RUBY:
                img = pygame.image.load("./data/img/ruby.png")
                img = pygame.transform.scale(img, size)
                images.append(img)
            elif s == Stones.SAPHYR:
                img = pygame.image.load("./data/img/sapphire.png")
                img = pygame.transform.scale(img, size)
                images.append(img)
        return images

    def mapDisplay(self, map, screen, x, y):
        if map:
            img_map = pygame.image.load("./data/img/map.png")
            img_map = pygame.transform.scale(img_map, (70, 70))
            screen.blit(img_map, (x, y))
            return img_map
        return None


    def questDisplay(self):
        return QuestDisplay(self.card.quest, self.screen, self.width, self.height)


    def clickIn(self, coord_clic):
        return self.rect.collidepoint(coord_clic[0], coord_clic[1])


    def display(self, x, y):
        self.rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(self.screen, self.colorToColor(self.card.color), self.rect, border_radius=30) 
        r = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(self.screen, (255,255,255), r, 3, border_radius=30)
        images = self.stoneToImage(self.card.stones)
        last_x = 0
        for img in images:
            self.screen.blit(img, (x+self.width-img.get_width()+last_x-10, y+10))
            last_x -= img.get_width()

        self.mapDisplay(self.card.map, self.screen, x+self.width/4, y+10)

        self.questDisplay().display(x, y)