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
        transp = pygame.Surface((x, y), pygame.SRCALPHA)
        transp.fill((0, 0, 0, 0))
        sizePol = 60
        police = pygame.font.Font(None, sizePol)
        r = pygame.Rect(0,0,0,0)
        textr = ""
        div = 5

        points = self.quest.points
        if points != "0":
            if self.quest.conditionMode == ConditionModes.NOTHING:
                r = pygame.Rect(x-self.width/div-sizePol/(div-2), y-self.height/div, 100, 50)
                textr = points
            elif self.quest.conditionMode == ConditionModes.NIGHT:
                r = pygame.Rect(x-self.width/div-sizePol/(div-2), y-self.height/div, 100, 50)
                img_day = pygame.image.load("./data/img/night.png")
                img_day = pygame.transform.scale(img_day, (60, 60))
                textr = "= "+points
                self.screen.blit(img_day, (x-self.width/(div-2)-sizePol/(div-2), y-self.height/div))

        pygame.draw.rect(transp, (0,0,0), r)
        texte_surface = police.render(textr, True, (0,0,0))  
        self.screen.blit(texte_surface, (r.x + 5, r.y + 5))


    def display(self, x, y):
        self.conditionDisplay(x+self.width, y+self.height)

        

