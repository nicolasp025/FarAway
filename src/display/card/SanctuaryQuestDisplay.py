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

    font_size_coef          = 0.09

    img_size_coef           = 0.1
    imgPoints_posX_coef     = 0.34
    imgPoints_posY_coef     = 0.24
    points_posX_coef        = 0.21
    points_posY_coef        = 0.15

    night_posX_coef         = 0.72
    night_posY_coef         = 0.24

    equal_posX_coef         = 0.44
    equal_posY_coef         = 0.22

    map_posX_coef           = 0.72
    map_posY_coef           = 0.24

    stone_size_coef         = 0.08
    stone_posX_coef         = 0.67
    stone_posY_coef         = 0.22

    color_size_coef         = 0.065
    color_posX_coef         = 0.63
    color_posY_coef         = 0.21

    slash_size_coef         = 0.14    
    slash_posX_coef         = 0.67
    slash_posY_coef         = 0.15

    someColor_space_coef    = 0.08
    someColor_posX_coef     = 0.82
    someColor_posY_coef     = 0.26


    def __init__(self, quest, screen, width:int, height:int):
        super().__init__(quest, screen, width, height)
        self.policeSize = int(SanctuaryQuestDisplay.font_size_coef * (width + height))
        self.police = pygame.font.Font(None, self.policeSize)

        self.display_methods = {
            ConditionModes.NIGHT: self.displayNightCondition,
            ConditionModes.MAP: self.displayMapCondition,
            ConditionModes.STONE: self.displayStoneCondition,
            ConditionModes.COLOR: self.displayColorCondition,
            ConditionModes.SOMECOLOR: self.displaySomeColorCondition
        }

    ## Display the quest
    def display(self, x:int, y:int) -> None:
        self.conditionDisplay(x+self.width, y+self.height)

    ## Display the condition of the quest
    def conditionDisplay(self, x:int, y:int) -> None:
        if self.quest.points!=0:
            self.displayPoints(x, y)
            if self.quest.conditionMode != ConditionModes.NOTHING:
                self.display_methods[self.quest.conditionMode](x, y)
                self.displayEqual(x, y)       
            

    def displayNightCondition(self, x:int, y:int) -> None:
        # Load and display the night icon
        size = SanctuaryQuestDisplay.img_size_coef * (self.width + self.height)
        img_day = pygame.image.load("./data/img/night.png")
        img_day = pygame.transform.scale(img_day, (size, size))
        self.screen.blit(img_day, (x-self.width*SanctuaryQuestDisplay.night_posX_coef, y-self.height*SanctuaryQuestDisplay.night_posY_coef))

    def displayMapCondition(self, x:int, y:int) -> None:
        # Load and display the map icon
        img_map = pygame.image.load("./data/img/map.png")
        size = SanctuaryQuestDisplay.img_size_coef * (self.width + self.height)
        img_map = pygame.transform.scale(img_map, (size, size))
        self.screen.blit(img_map, (x-self.width*SanctuaryQuestDisplay.map_posX_coef, y-self.height*SanctuaryQuestDisplay.map_posY_coef))

    def displayStoneCondition(self, x:int, y:int) -> None:
        # Load and display the image of the stone within the condition
        stoneImages = Stones.stonesToImage(self.quest.condition, size=SanctuaryQuestDisplay.stone_size_coef * (self.width + self.height))
        self.screen.blit(stoneImages[0], (x-self.width*SanctuaryQuestDisplay.stone_posX_coef, y-self.height*SanctuaryQuestDisplay.stone_posY_coef))

    def displayColorCondition(self, x:int, y:int) -> None:
        i=0
        imgSize = SanctuaryQuestDisplay.color_size_coef * (self.width + self.height)
        slashFontSize = int(SanctuaryQuestDisplay.slash_size_coef * (self.width + self.height))
        colorImages = Colors.colorsToImage(self.quest.condition, imgSize)
        spaceBetween = imgSize / 2
        # Display the color(s) within the condition
        for color in colorImages:
            tmpY = y-self.height*SanctuaryQuestDisplay.color_posY_coef
            if i==0:
                tmpX = x-self.width*SanctuaryQuestDisplay.color_posX_coef
                self.screen.blit(color, (tmpX, tmpY))
            else:
                tmpX = x-self.width*SanctuaryQuestDisplay.color_posX_coef-(i*imgSize)-spaceBetween
                self.screen.blit(color, (tmpX, tmpY)) 
            i+=1
        
        # Add separators between the colors
        if len(self.quest.condition) > 1:
                tmpPol = pygame.font.Font(None, slashFontSize)
                texte_surface = tmpPol.render("/", True, (0,0,0))
                r = texte_surface.get_rect()
                r.center = (x-self.width*SanctuaryQuestDisplay.slash_posX_coef, y-self.height*SanctuaryQuestDisplay.slash_posY_coef)
                self.screen.blit(texte_surface, r)

    def displaySomeColorCondition(self, x:int, y:int) -> None:
        i=0
        imgSize = SanctuaryQuestDisplay.color_size_coef * (self.width + self.height)
        spaceBetween = imgSize * SanctuaryQuestDisplay.someColor_space_coef
        colorImages = Colors.colorsToImage(self.quest.condition, imgSize)
        # Display the colors
        for color in colorImages:
            addOnRow = 0 if i%2==0 else imgSize+spaceBetween
            addOnColomn = (i//2)*(imgSize + spaceBetween)
            tmpX = x-self.width*SanctuaryQuestDisplay.someColor_posX_coef+addOnRow
            tmpY = y-self.height*SanctuaryQuestDisplay.someColor_posY_coef+addOnColomn
            self.screen.blit(color, (tmpX, tmpY))
            i+=1
    
    def displayEqual(self, x:int, y:int) -> None:
        if self.quest.conditionMode != ConditionModes.NOTHING:
            text_eg = self.police.render("=", True, (0,0,0)) 
            self.screen.blit(text_eg, (x-self.width*SanctuaryQuestDisplay.equal_posX_coef, y-self.height*SanctuaryQuestDisplay.equal_posY_coef))  
    
    def displayPoints(self, x:int, y:int) -> None:
        # Setup the image for the background of the points and display it
        img_pt = pygame.image.load("./data/img/points.png")
        imgSize = SanctuaryQuestDisplay.img_size_coef * (self.width + self.height)
        img_pt = pygame.transform.scale(img_pt, (imgSize, imgSize))
        self.screen.blit(img_pt, (x-self.width*SanctuaryQuestDisplay.imgPoints_posX_coef, y-self.height*SanctuaryQuestDisplay.imgPoints_posY_coef))

        # Display the points
        points = self.quest.points
        texte_surface = self.police.render(str(points), True, (0,0,0))
        r = texte_surface.get_rect()
        r.center = (x-self.width*SanctuaryQuestDisplay.points_posX_coef, y-self.height*SanctuaryQuestDisplay.points_posY_coef)
        self.screen.blit(texte_surface, r)

