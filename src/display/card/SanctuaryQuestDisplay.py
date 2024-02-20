import pygame
import sys

sys.path.append("./src/enum/")
from ConditionModes import ConditionModes
from Colors import Colors
from Stones import Stones
from Quest import Quest
from QuestDisplay import QuestDisplay


class SanctuaryQuestDisplay(QuestDisplay):

    def __init__(self, quest, screen, cardWidth, cardHeight):
        super().__init__(quest, screen, cardWidth, cardHeight)
    
    def display(self, x, y):
        self.conditionDisplay(x+self.width, y+self.height)

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

            elif self.quest.conditionMode == ConditionModes.NIGHT:
                r = pygame.Rect(x-self.width/div-sizePol/(div-2), y-self.height/div, 100, 50)
                img_day = pygame.image.load("./data/img/night.png")
                img_day = pygame.transform.scale(img_day, (60, 60))
                self.screen.blit(img_day, (x-self.width*0.7, y-self.height*0.22))

            elif self.quest.conditionMode == ConditionModes.MAP:
                r = pygame.Rect(x-self.width/div-sizePol/(div-2), y-self.height/div, 100, 50)
                img_map = pygame.image.load("./data/img/map.png")
                img_map = pygame.transform.scale(img_map, (60, 60))
                self.screen.blit(img_map, (x-self.width*0.7, y-self.height*0.22))

            elif self.quest.conditionMode == ConditionModes.STONE:
                stoneImages = Stones.stonesToImage(self.quest.condition)
                for i in range(len(stoneImages)):
                    stoneImages[i] = pygame.transform.scale(stoneImages[i], (50, 50))
                    self.screen.blit(stoneImg, (x*i*0.68, y*i*0.18))

            elif self.quest.conditionMode == ConditionModes.COLOR:
                i=0
                max = len(self.quest.condition)
                for color in self.quest.condition:
                    colorImg = pygame.image.load("./data/img/"+Colors.toStringLower(color)+".png")
                    colorImg = pygame.transform.scale(colorImg, (40, 40))
                    self.screen.blit(colorImg, (x-self.width/(div-3)-sizePol/(div)-i*60, y-self.height/div+10))
                    i+=1
                    if i != max:
                        tmpPol = pygame.font.Font(None, sizePol + 45)
                        texte_surface = tmpPol.render("/", True, (0,0,0))
                        r = texte_surface.get_rect()
                        r.center = (x-self.width*0.68-i*10, y-self.height*0.2)
                        self.screen.blit(texte_surface, r)

            elif self.quest.conditionMode == ConditionModes.SOMECOLOR:
                i=0
                for color in self.quest.condition:
                    colorImg = pygame.image.load("./data/img/"+Colors.toStringLower(color)+".png")
                    colorImg = pygame.transform.scale(colorImg, (40, 40))
                    if i%2==0:
                        self.screen.blit(colorImg, (x-self.width/(div-3)-sizePol/(div)-i*22, y-self.height/div+10))
                    else:
                        self.screen.blit(colorImg, (x-self.width/(div-3)-sizePol/(div)-(i-1)*22, y-self.height/div+10-43))
                    i+=1

            textr = points
            textr = str(textr)

            pygame.draw.rect(transp, (0, 0, 255), rect)
            
            if self.quest.conditionMode != ConditionModes.NOTHING: 
                self.screen.blit(text_eg, (x-self.width*0.41, y-self.height*0.19))

            texte_surface = police.render(textr, True, (0,0,0))
            r = texte_surface.get_rect()
            r.center = (x-self.width*0.15, y-self.height*0.13) # Display the number of points
    
            self.screen.blit(img_pt, (x-self.width*0.3, y-self.height*0.22)) # Display the points square
            self.screen.blit(texte_surface, r)