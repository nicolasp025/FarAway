import pygame
import sys

sys.path.append("./src/enum/")
from ConditionModes import ConditionModes
from Colors import Colors
from Stones import Stones
from Quest import Quest
from QuestDisplay import QuestDisplay

## The class to represent the display of a region quest card
class RegionQuestDisplay(QuestDisplay):

    font_size_coef                  = 0.14
    imgPoints_size_coef             = 0.17

    require_imgSize_coef            = 0.12
    require_color1_coef             = 1.1
    require_color2_coef             = 0.6
    require_posY_coef               = 0.55
    require_posX_coef               = 0.02
    require_width_coef              = 0.055
    require_borderRadius_coef       = 0.06
    require_stone_posX_coef         = 0.065
    require_stone_posY_coef         = 0.02

    quest_background_posY_coef      = 0.275
    quest_background_height_coef    = 0.25
    quest_background_posX_coef      = 0.67
    quest_background_width_coef     = 0.62

    nothing_background_width_coef   = 0.27
    nothing_background_posX_coef    = 0.35

    color_background_posX_coef      = 0.77
    color_background_width_coef     = 0.72

    night_size_coef                 = 0.15
    night_posX_coef                 = 0.59
    night_posY_coef                 = 0.23
    
    map_size_coef                   = 0.15
    map_posX_coef                   = 0.59
    map_posY_coef                   = 0.23

    stone_size_coef                 = 0.13
    stone_posX_coef                 = 0.58
    stone_posY_coef                 = 0.22

    color_size_coef                 = 0.1
    color_posX_coef                 = 0.56
    color_posY_coef                 = 0.21

    def __init__(self, quest, screen, width:int, height:int):
        super().__init__(quest, screen, width, height)
        # Setup police
        self.policeSize = int(self.width*RegionQuestDisplay.font_size_coef)
        self.police = pygame.font.Font(None, self.policeSize)
        tmpSize = width*RegionQuestDisplay.imgPoints_size_coef
        self.pointsSize = (tmpSize, tmpSize)

        self.display_methods = {
            ConditionModes.NIGHT: self.displayNightCondition,
            ConditionModes.MAP: self.displayMapCondition,
            ConditionModes.STONE: self.displayStoneCondition,
            ConditionModes.COLOR: self.displayColorCondition,
            ConditionModes.SOMECOLOR: self.displaySomeColorCondition
        }

    ## Display the require of the quest
    def requireDisplay(self, x:int, y:int, color:tuple[int, int, int]) -> None:
        l = []
        sizeImg = self.width*RegionQuestDisplay.require_imgSize_coef

        # Create a list with all the stones required
        for key in self.quest.require:
            for i in range(self.quest.require.get(key)):
                l.append(key)

        r, g, b = color

        # Set the color of the rectangle
        newr = min(int(r * RegionQuestDisplay.require_color1_coef), 255)
        newg = min(int(g * RegionQuestDisplay.require_color1_coef), 255)
        newb = min(int(b * RegionQuestDisplay.require_color1_coef), 255)
        col = (newr, newg, newb)

        # Set the color of the border
        newr = min(int(r * RegionQuestDisplay.require_color2_coef), 255)
        newg = min(int(g * RegionQuestDisplay.require_color2_coef), 255)
        newb = min(int(b * RegionQuestDisplay.require_color2_coef), 255)
        col2 = (newr, newg, newb)

        if len(l) > 0:
            # Display the rectangle for the require
            requireY = y-self.height*RegionQuestDisplay.require_posY_coef
            requireHeight = sizeImg*1.5
            requireX = x-(len(l)+1)*sizeImg + self.width * RegionQuestDisplay.require_posX_coef
            requireWidth = (len(l)+1)*sizeImg - self.width * RegionQuestDisplay.require_width_coef
            r1 = pygame.Rect(requireX, requireY, requireWidth, requireHeight)

            tmpRadius = int(RegionQuestDisplay.require_borderRadius_coef * (requireHeight + requireWidth))
            pygame.draw.rect(self.screen, col, r1, border_radius=tmpRadius)
            pygame.draw.rect(self.screen, col2, r1, 3, border_radius=tmpRadius)

            # Display the stones
            addOn = -self.width*0.01 if len(l)==1 else 0
            i = 1
            for img_stone in Stones.stonesToImage(l, sizeImg):
                tmpX = x-sizeImg*i-self.width*RegionQuestDisplay.require_stone_posX_coef+addOn
                tmpY = requireY + self.height*RegionQuestDisplay.require_stone_posY_coef
                self.screen.blit(img_stone, (tmpX, tmpY))
                i += 1

        if self.quest.points != 0:
            # Display the background of the quest
            rY = y-self.height*RegionQuestDisplay.quest_background_posY_coef
            rHeight = self.height*RegionQuestDisplay.quest_background_height_coef
            if self.quest.conditionMode == ConditionModes.NOTHING:
                rWidth = self.width*RegionQuestDisplay.nothing_background_width_coef
                rX = x - self.width*RegionQuestDisplay.nothing_background_posX_coef
            elif self.quest.conditionMode == ConditionModes.SOMECOLOR or self.quest.conditionMode == ConditionModes.COLOR:
                rX = x-self.width*RegionQuestDisplay.color_background_posX_coef
                rWidth = self.width*RegionQuestDisplay.color_background_width_coef
            else:
                rX = x-self.width*RegionQuestDisplay.quest_background_posX_coef
                rWidth = self.width*RegionQuestDisplay.quest_background_width_coef

            r2 = pygame.Rect(rX, rY, rWidth, rHeight)
            pygame.draw.rect(self.screen, col, r2, border_radius=50)
            pygame.draw.rect(self.screen, col2, r2, 3, border_radius=50)
                
        self.displayPoints(x, y)
        

    ## Display the condition of the quest
    def conditionDisplay(self, x:int, y:int) -> None:

        # Set the images and text to display depending of the condition mode
        if self.quest.points != 0 and self.quest.conditionMode != ConditionModes.NOTHING:
            self.display_methods[self.quest.conditionMode](x, y)
            self.displayEqual(x, y)
    
    def displayNightCondition(self, x, y):
        # Load and display the night image
        img_night = pygame.image.load("./data/img/night.png")
        nightSize = self.width * RegionQuestDisplay.night_size_coef
        img_night = pygame.transform.scale(img_night, (nightSize, nightSize))
        tmpX = x - self.width * RegionQuestDisplay.night_posX_coef
        tmpY = y - self.height * RegionQuestDisplay.night_posY_coef
        self.screen.blit(img_night, (tmpX, tmpY))

    def displayMapCondition(self, x, y):
        # Load and display the map image
        img_map = pygame.image.load("./data/img/map.png")
        sizeMap = self.width*RegionQuestDisplay.map_size_coef
        img_map = pygame.transform.scale(img_map, (sizeMap, sizeMap))
        tmpX = x - self.width * RegionQuestDisplay.map_posX_coef
        tmpY = y - self.height * RegionQuestDisplay.map_posY_coef
        self.screen.blit(img_map, (tmpX, tmpY))
    
    def displayStoneCondition(self, x, y):
        # Load and display the image of the stone within the condition
        sizeStone = self.width * RegionQuestDisplay.stone_size_coef
        stoneImages = Stones.stonesToImage(self.quest.condition, sizeStone)
        tmpX = x - self.width * RegionQuestDisplay.stone_posX_coef
        tmpY = y - self.height * RegionQuestDisplay.stone_posY_coef
        self.screen.blit(stoneImages[0], (tmpX, tmpY))

    def displayColorCondition(self, x, y):
        i=0
        max = len(self.quest.condition) # The number of color to display
        imgSize = self.width * RegionQuestDisplay.color_size_coef
        colorImages = Colors.colorsToImage(self.quest.condition, imgSize)

        # Display the image for all color within the condition 
        for color in colorImages:
            if i==0:
                self.screen.blit(color, (x-self.width*RegionQuestDisplay.color_posX_coef, y-self.height*RegionQuestDisplay.color_posY_coef))
            else:
                self.screen.blit(color, (x-self.width*RegionQuestDisplay.color_posX_coef-(i*imgSize)-imgSize/2, y-self.height*RegionQuestDisplay.color_posY_coef)) 
            i+=1
            
            # Separate the next image representing a color
            if i != max:
                tmpPol = pygame.font.Font(None, int(self.policeSize * 1.6))
                texte_surface = tmpPol.render("/", True, (0,0,0))
                r = texte_surface.get_rect()
                r.center = (x-self.width*0.49-i*self.width*0.1, y-self.height*0.15)
                self.screen.blit(texte_surface, r)
    
    def displaySomeColorCondition(self, x, y):
        # Display all colors
        i=0
        ImgSize = self.height*0.1
        colorImages = Colors.colorsToImage(self.quest.condition, ImgSize)
        for color in colorImages:
            if i%2==0:
                self.screen.blit(color, (x-self.width*0.55-i*self.width*0.055, y-self.height*0.15))
            else:
                self.screen.blit(color, (x-self.width*0.55-(i-1)*self.width*0.055, y-self.height*0.15-ImgSize*1.09))
            i+=1

    def displayEqual(self, x, y):
        # If there is any condition display the equal
        if self.quest.conditionMode != ConditionModes.NOTHING: 
            text_eg = self.police.render("=", True, (0,0,0))
            self.screen.blit(text_eg, (x-self.width*0.4, self.pointsCoords[1]+(self.pointsSize[1]/6)))

    def displayPoints(self, x, y):
        if (self.quest.points > 0):
            # Setup the image for the background of the points and display it
            img_pt = pygame.image.load("./data/img/points.png")
            img_pt = pygame.transform.scale(img_pt, self.pointsSize)
            self.pointsCoords = (x-self.width*0.3, y-self.height*0.24)
            self.screen.blit(img_pt, self.pointsCoords)

            # Display the points
            texte_surface = self.police.render(str(self.quest.points), True, (0,0,0))
            r = texte_surface.get_rect()
            r.center = (x-self.width*0.218, y-self.height*0.15)
            self.screen.blit(texte_surface, r)