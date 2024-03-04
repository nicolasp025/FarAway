import pygame
import sys

sys.path.append("./src/enum/")
from ConditionModes import ConditionModes
from Colors import Colors
from Stones import Stones
from Quest import Quest
from QuestDisplay import QuestDisplay

## The class which represent the display of the quest for the sanctuary cards
class SanctuaryQuestDisplay(QuestDisplay):

    def __init__(self, quest, screen, cardWidth:int, cardHeight:int):
        super().__init__(quest, screen, cardWidth, cardHeight)
    

    ## Display the quest
    def display(self, x:int, y:int) -> None:
        self.conditionDisplay(x+self.width, y+self.height)

    ## Display the condition of the quest
    def conditionDisplay(self, x:int, y:int) -> None:
        # Set the polices
        sizePol = 50
        police = pygame.font.Font(None, sizePol)

        points = self.quest.points
        if points != 0:
            # Setup the image for the background of the points and display it
            img_pt = pygame.image.load("./data/img/points.png")
            img_pt = pygame.transform.scale(img_pt, (60, 60))
            self.screen.blit(img_pt, (x-self.width*0.3, y-self.height*0.22))

            if self.quest.conditionMode == ConditionModes.NIGHT:
                # Load and display the night icon
                img_day = pygame.image.load("./data/img/night.png")
                img_day = pygame.transform.scale(img_day, (60, 60))
                self.screen.blit(img_day, (x-self.width*0.7, y-self.height*0.22))
            elif self.quest.conditionMode == ConditionModes.MAP:
                # Load and display the map icon
                img_map = pygame.image.load("./data/img/map.png")
                img_map = pygame.transform.scale(img_map, (60, 60))
                self.screen.blit(img_map, (x-self.width*0.7, y-self.height*0.22))
            elif self.quest.conditionMode == ConditionModes.STONE:
                # Load and display the image of the stone within the condition
                stoneImages = Stones.stonesToImage(self.quest.condition, 50)
                self.screen.blit(stoneImages[0], (x-self.width*0.69, y-self.height*0.21))
            elif self.quest.conditionMode == ConditionModes.COLOR:
                i=0
                imgSize = 40
                fontSize = 45
                colorImages = Colors.colorsToImage(self.quest.condition, imgSize)
                # Display the color(s) within the condition
                for color in colorImages:
                    if i==0:
                        self.screen.blit(color, (x-self.width*0.63, y-self.height*0.19))
                    else:
                        self.screen.blit(color, (x-self.width*0.63-(i*imgSize)-20, y-self.height*0.19)) 
                    i+=1
                
                # Add separators between the colors
                if len(self.quest.condition) > 1:
                        tmpPol = pygame.font.Font(None, sizePol + fontSize)
                        texte_surface = tmpPol.render("/", True, (0,0,0))
                        r = texte_surface.get_rect()
                        r.center = (x-self.width*0.67, y-self.height*0.13)
                        self.screen.blit(texte_surface, r)
            elif self.quest.conditionMode == ConditionModes.SOMECOLOR:
                i=0
                spaceBetween = 3
                imgSize = 40
                colorImages = Colors.colorsToImage(self.quest.condition, imgSize)
                # Display the colors
                for color in colorImages:
                    addOn = 0 if i%2==0 else imgSize+spaceBetween
                    self.screen.blit(color, (x-self.width*0.58+addOn, y-self.height*0.19-addOn))
                    i+=1
            
            # Display the equal
            if self.quest.conditionMode != ConditionModes.NOTHING:
                text_eg = police.render("=", True, (0,0,0)) 
                self.screen.blit(text_eg, (x-self.width*0.41, y-self.height*0.19))  

            # Display the points
            texte_surface = police.render(str(points), True, (0,0,0))
            r = texte_surface.get_rect()
            r.center = (x-self.width*0.15, y-self.height*0.13)
            self.screen.blit(texte_surface, r)