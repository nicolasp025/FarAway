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

    def mapDisplay(self):
        if self.card.map:
            img_map = pygame.image.load("./data/img/map.png")
            img_map = pygame.transform.scale(img_map, (70, 70))
            return img_map
        return None


    def questDisplay(self):
        return QuestDisplay(self.card.quest, self.screen, self.width, self.height)


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
            colors =  (255, 99, 71), (220, 20, 60)
        elif self.card.color ==  Colors.BLUE:
            colors =  (135, 206, 250), (0, 0, 139)
        elif self.card.color == Colors.YELLOW:
            colors =  (255, 255, 102), (255, 215, 0)
        elif self.card.color == Colors.GRAY:
            colors = (192, 192, 192), (128, 128, 128)
        return colors, rect1, rect2
        
    def banner(self):
        img = None
        if self.card.color == Colors.GREEN:
            img = pygame.image.load("./data/img/green_banner.png")
        elif self.card.color == Colors.RED:
            img = pygame.image.load("./data/img/red_banner.png")
        elif self.card.color == Colors.BLUE:
            img = pygame.image.load("./data/img/blue_banner.png")
        elif self.card.color == Colors.YELLOW:
            img = pygame.image.load("./data/img/yellow_banner.png")
        elif self.card.color == Colors.GRAY:
            img = pygame.image.load("./data/img/gray_banner.png")
        img = pygame.transform.scale(img, (self.width, 35))
        return img
    
    def display(self, x, y):
        (col1, col2), rect1, rect2 = self.backgroundColor(x, y)
        pygame.draw.rect(self.screen, col1, rect1, border_radius=30) 
        pygame.draw.rect(self.screen, col2, rect2, border_radius=30)
        self.screen.blit(self.banner(), (x, y+(self.height/3)*2-15)) 
        r = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(self.screen, (255,255,255), r, 3, border_radius=30)
        images = self.stoneToImage(self.card.stones)
        last_x = 0
        for img in images:
            self.screen.blit(img, (x+self.width-img.get_width()+last_x-10, y+10))
            last_x -= img.get_width()

        img_map = self.mapDisplay()
        if img_map != None:
            self.screen.blit(img_map, (x+self.width/4, y+10))

        self.questDisplay().display(x, y)