import pygame
import sys

sys.path.append("./src/enum/")
from ConditionModes import ConditionModes
from Colors import Colors
from Stones import Stones
from Quest import Quest
from QuestDisplay import QuestDisplay


class RegionQuestDisplay(QuestDisplay):

    def __init__(self, quest, screen, cardWidth, cardHeight):
        super().__init__(quest, screen, cardWidth, cardHeight)

    def requireDisplay(self, x, y, color):
        l = []
        sizeImg = 35
        for key in self.quest.require:
            for i in range(self.quest.require.get(key)):
                l.append(key)

        if len(l) > 0:
            r, g, b = color
            f1 = 1.1
            newr = min(int(r * f1), 255)
            newg = min(int(g * f1), 255)
            newb = min(int(b * f1), 255)
            col1 = (newr, newg, newb)
            f2 = 0.9
            newr = min(int(r * f2), 255)
            newg = min(int(g * f2), 255)
            newb = min(int(b * f2), 255)
            col2 = (newr, newg, newb)
            x2, y2 = x-(len(l)+1)*sizeImg, y-self.height*0.51
            r = pygame.Rect(x2, y2, (len(l)+1)*sizeImg-15, 160)
            pygame.draw.rect(self.screen, col1, r, border_radius=10)
            pygame.draw.rect(self.screen, col2, r, 2, border_radius=10)

            i = 1
            for img_stone in Stones.stonesToImage(l, sizeImg):
                self.screen.blit(img_stone, (x-sizeImg*i-25, y-self.height*0.49))
                i += 1

    def conditionDisplay(self, x, y):
        sizePol = 50
        police = pygame.font.Font(None, sizePol)
        img_pt = pygame.image.load("./data/img/points.png")
        img_pt = pygame.transform.scale(img_pt, (65, 60))

        rect = pygame.Rect(x, y, 50, 50)
        transp = pygame.Surface((200, 100), pygame.SRCALPHA)
        transp.fill((255, 255, 255, 0))
        text_eg = police.render("=", True, (0,0,0))

        textr = ""
        div = 5

        points = self.quest.points
        if points != 0:
            if self.quest.conditionMode == ConditionModes.NOTHING:
                r = pygame.Rect(x-self.width/div-sizePol/(div-2), y-self.height/div, 100, 50)
                textr = points
            elif self.quest.conditionMode == ConditionModes.NIGHT:
                r = pygame.Rect(x-self.width/div-sizePol/(div-2), y-self.height/div, 100, 50)
                img_day = pygame.image.load("./data/img/night.png")
                img_day = pygame.transform.scale(img_day, (60, 60))
                textr = points
                self.screen.blit(img_day, (x-self.width*0.67, y-self.height*0.22))
            elif self.quest.conditionMode == ConditionModes.MAP:
                r = pygame.Rect(x-self.width/div-sizePol/(div-2), y-self.height/div, 100, 50)
                img_map = pygame.image.load("./data/img/map.png")
                img_map = pygame.transform.scale(img_map, (60, 60))
                textr = points
                self.screen.blit(img_map, (x-self.width*0.67, y-self.height*0.22))
            elif self.quest.conditionMode == ConditionModes.STONE:
                img = None
                stone = self.quest.condition[0]
                if stone == Stones.EMERALD:
                    img = pygame.image.load("./data/img/emerald.png")
                elif stone == Stones.RUBY:
                    img = pygame.image.load("./data/img/ruby.png")
                elif stone == Stones.SAPPHIRE:
                    img = pygame.image.load("./data/img/sapphire.png")
                img = pygame.transform.scale(img, (50, 50))
                self.screen.blit(img, (x-self.width*0.65, y-self.height*0.2))
                textr = points
            elif self.quest.conditionMode == ConditionModes.COLOR:
                i=0
                max = len(self.quest.condition)
                for color in self.quest.condition:
                    img = None
                    if color == Colors.BLUE:
                        img = pygame.image.load("./data/img/blue.png")
                    elif color == Colors.RED:
                        img = pygame.image.load("./data/img/red.png")
                    elif color == Colors.YELLOW:
                        img = pygame.image.load("./data/img/yellow.png")
                    elif color == Colors.GREEN:
                        img = pygame.image.load("./data/img/green.png")
                    img = pygame.transform.scale(img, (40, 40))
                    self.screen.blit(img, (x-self.width*0.63-i*60, y-self.height*0.19))
                    i+=1
                    if i != max:
                        tmpPol = pygame.font.Font(None, sizePol + 45)
                        texte_surface = tmpPol.render("/", True, (0,0,0))
                        r = texte_surface.get_rect()
                        r.center = (x-self.width*0.63-i*10, y-self.height*0.13)
                        self.screen.blit(texte_surface, r)
                textr = points
            elif self.quest.conditionMode == ConditionModes.SOMECOLOR:
                i=0
                for color in self.quest.condition:
                    img = None
                    if color == Colors.BLUE:
                        img = pygame.image.load("./data/img/blue.png")
                    elif color == Colors.RED:
                        img = pygame.image.load("./data/img/red.png")
                    elif color == Colors.YELLOW:
                        img = pygame.image.load("./data/img/yellow.png")
                    elif color == Colors.GREEN:
                        img = pygame.image.load("./data/img/green.png")
                    img = pygame.transform.scale(img, (40, 40))
                    if i%2==0:
                        self.screen.blit(img, (x-self.width*0.63-i*22, y-self.height*0.13))
                    else:
                        self.screen.blit(img, (x-self.width*0.63-(i-1)*22, y-self.height*0.13-43))
                    i+=1
                textr = points

            textr = str(textr)

            pygame.draw.rect(transp, (0, 0, 255), rect)
            
            if self.quest.conditionMode != ConditionModes.NOTHING: 
                self.screen.blit(text_eg, (x-self.width*0.47, y-self.height*0.19))

            texte_surface = police.render(textr, True, (0,0,0))
            r = texte_surface.get_rect()
            r.center = (x-self.width*0.29, y-self.height*0.13) # Display the number of points
    
            self.screen.blit(img_pt, (x-self.width*0.375, y-self.height*0.22)) # Display the points square
            self.screen.blit(texte_surface, r)
    