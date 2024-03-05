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
        self.policeSize = 50
        self.police = pygame.font.Font(None, self.policeSize)
    

    ## Display the quest
    def display(self, x:int, y:int) -> None:
        self.conditionDisplay(x+self.width, y+self.height)

    ## Display the condition of the quest
    def conditionDisplay(self, x:int, y:int) -> None:
        if self.quest.points==0:
            return

        if self.quest.conditionMode == ConditionModes.NIGHT:
            self.displayNightCondition(x, y)

        elif self.quest.conditionMode == ConditionModes.MAP:
            self.displayMapCondition(x, y)

        elif self.quest.conditionMode == ConditionModes.STONE:
            self.displayStoneCondition(x, y)

        elif self.quest.conditionMode == ConditionModes.COLOR:
            self.displayColorCondition(x, y)

        elif self.quest.conditionMode == ConditionModes.SOMECOLOR:
            self.displaySomeColorCondition(x, y)

        self.displayEqual(x, y)
        self.displayPoints(x, y)

    def displayNightCondition(self, x:int, y:int) -> None:
        # Load and display the night icon
        img_day = pygame.image.load("./data/img/night.png")
        img_day = pygame.transform.scale(img_day, (60, 60))
        self.screen.blit(img_day, (x-self.width*0.7, y-self.height*0.22))

    def displayMapCondition(self, x:int, y:int) -> None:
        # Load and display the map icon
        img_map = pygame.image.load("./data/img/map.png")
        img_map = pygame.transform.scale(img_map, (60, 60))
        self.screen.blit(img_map, (x-self.width*0.7, y-self.height*0.22))

    def displayStoneCondition(self, x:int, y:int) -> None:
        # Load and display the image of the stone within the condition
        stoneImages = Stones.stonesToImage(self.quest.condition, 50)
        self.screen.blit(stoneImages[0], (x-self.width*0.69, y-self.height*0.21))

    def displayColorCondition(self, x:int, y:int) -> None:
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
                tmpPol = pygame.font.Font(None, self.policeSize + fontSize)
                texte_surface = tmpPol.render("/", True, (0,0,0))
                r = texte_surface.get_rect()
                r.center = (x-self.width*0.67, y-self.height*0.13)
                self.screen.blit(texte_surface, r)

    def displaySomeColorCondition(self, x:int, y:int) -> None:
        i=0
        spaceBetween = 3
        imgSize = 40
        colorImages = Colors.colorsToImage(self.quest.condition, imgSize)
        # Display the colors
        for color in colorImages:
            addOnRow = 0 if i%2==0 else imgSize+spaceBetween
            addOnColomn = (i//2)*(imgSize + spaceBetween)
            tmpX = x-self.width*0.84+addOnRow
            tmpY = y-self.height*0.26+addOnColomn
            self.screen.blit(color, (tmpX, tmpY))
            i+=1
    
    def displayEqual(self, x:int, y:int) -> None:
        if self.quest.conditionMode != ConditionModes.NOTHING:
            text_eg = self.police.render("=", True, (0,0,0)) 
            self.screen.blit(text_eg, (x-self.width*0.41, y-self.height*0.19))  
    
    def displayPoints(self, x:int, y:int) -> None:
        # Setup the image for the background of the points and display it
        img_pt = pygame.image.load("./data/img/points.png")
        img_pt = pygame.transform.scale(img_pt, (60, 60))
        self.screen.blit(img_pt, (x-self.width*0.3, y-self.height*0.22))

        # Display the points
        points = self.quest.points
        texte_surface = self.police.render(str(points), True, (0,0,0))
        r = texte_surface.get_rect()
        r.center = (x-self.width*0.15, y-self.height*0.13)
        self.screen.blit(texte_surface, r)

