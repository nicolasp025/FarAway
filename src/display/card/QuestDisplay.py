import pygame
import sys

sys.path.append("./src/enum/")
from ConditionModes import ConditionModes
from Colors import Colors
from Stones import Stones
from Quest import Quest


class QuestDisplay():

    def __init__(self, quest, screen, cardWidth, cardHeight):
        self.quest = quest
        self.screen = screen
        self.width = cardWidth
        self.height = cardHeight


    def conditionDisplay(self, x, y):
        sizePol = 50
        police = pygame.font.Font(None, sizePol)
        img_pt = pygame.image.load("./data/img/points.png")
        img_pt = pygame.transform.scale(img_pt, (60, 60))

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
                self.screen.blit(img_day, (x-self.width/(div-3)-sizePol/(div-2), y-self.height/div))
            elif self.quest.conditionMode == ConditionModes.MAP:
                r = pygame.Rect(x-self.width/div-sizePol/(div-2), y-self.height/div, 100, 50)
                img_map = pygame.image.load("./data/img/map.png")
                img_map = pygame.transform.scale(img_map, (60, 60))
                textr = points
                self.screen.blit(img_map, (x-self.width/(div-3)-sizePol/(div-2), y-self.height/div))
            elif self.quest.conditionMode == ConditionModes.STONE:
                img = None
                stone = self.quest.condition[0]
                if stone == Stones.EMERALD:
                    img = pygame.image.load("./data/img/emerald.png")
                elif stone == Stones.RUBY:
                    img = pygame.image.load("./data/img/ruby.png")
                elif stone == Stones.SAPHYR:
                    img = pygame.image.load("./data/img/sapphire.png")
                img = pygame.transform.scale(img, (45, 50))
                self.screen.blit(img, (x-self.width/(div-3)-sizePol/(div), y-self.height/div+5))
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
                    self.screen.blit(img, (x-self.width/(div-3)-sizePol/(div)-i*60, y-self.height/div+10))
                    i+=1
                    if i != max:
                        tmpPol = pygame.font.Font(None, sizePol + 45)
                        texte_surface = tmpPol.render("/", True, (0,0,0))
                        r = texte_surface.get_rect()
                        r.center = (x-self.width/(div-3)-sizePol/(div)-i*10, y-self.height/(div+3)+3)
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
                        self.screen.blit(img, (x-self.width/(div-3)-sizePol/(div)-i*22, y-self.height/div+10))
                    else:
                        self.screen.blit(img, (x-self.width/(div-3)-sizePol/(div)-(i-1)*22, y-self.height/div+10-43))
                    i+=1
                textr = points

            textr = str(textr)

            pygame.draw.rect(transp, (0, 0, 255), rect)
            
            self.screen.blit(text_eg, (x-self.width/(div-2)-10, y-self.height/(div+1)-2))

            texte_surface = police.render(textr, True, (0,0,0))
            r = texte_surface.get_rect()
            r.center = (x-self.width/(div), y-self.height/(div+3)+3)
    
            self.screen.blit(img_pt, (x-self.width/(div-1)-sizePol/div, y-self.height/div))
            self.screen.blit(texte_surface, r)
        


    def display(self, x, y):
        self.conditionDisplay(x+self.width, y+self.height)

        

