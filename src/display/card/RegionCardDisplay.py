import pygame
import sys

sys.path.append("./src/card/")
sys.path.append("./src/enum/")
from RegionCard import RegionCard
from Colors import Colors
from Stones import Stones
from Quest import Quest

class RegionCardDisplay():

    def __init__(self, card, screen, clock, x, y, width, height):
        self.size = (width, height)
        self.card = card
        self.x = x
        self.y = y
        self.screen = screen
        self.clock = clock
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

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
        size = (40, 60)
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

    def mapDisplay(self, map, screen, x, y):
        if map:
            img_map = pygame.image.load("./data/img/map.png")
            img_map = pygame.transform.scale(img_map, (70, 70))
            screen.blit(img_map, (x, y))
            return img_map
        return None

    # def questDisplay(self, quest):

    def clickIn(self, coord_clic):
        return self.rect.collidepoint(coord_clic[0], coord_clic[1])


    def regionCardDisplay(self):
        pygame.draw.rect(self.screen, self.colorToColor(self.card.color), self.rect, border_radius=30) 
        images = self.stoneToImage(self.card.stones)
        last_x = 0
        for img in images:
            self.screen.blit(img, (self.x+self.width-img.get_width()+last_x-10, self.y+10))
            last_x -= img.get_width()

        img_day = self.dayDisplay(self.card.day)
        self.screen.blit(img_day, (self.x+10,self.y+10))

        self.screen.blit(self.idDisplay(self.card.id), (self.x+img_day.get_width()/2, self.y+img_day.get_height()/2-2))

        self.mapDisplay(self.card.map, self.screen, self.x+img_day.get_width()+20, self.y+10)
