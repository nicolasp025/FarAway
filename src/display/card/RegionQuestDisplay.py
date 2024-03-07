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

    def __init__(self, quest, screen, cardWidth:int, cardHeight:int):
        super().__init__(quest, screen, cardWidth, cardHeight)
        # Setup police
        self.policeSize = 50
        self.police = pygame.font.Font(None, self.policeSize)
        self.pointsSize = (60, 60)

    ## Display the require of the quest
    def requireDisplay(self, x:int, y:int, color:tuple[int, int, int]) -> None:
        l = []
        sizeImg = 35

        # Create a list with all the stones required
        for key in self.quest.require:
            for i in range(self.quest.require.get(key)):
                l.append(key)

        if len(l) > 0:
            r, g, b = color

            # Set the color of the rectangle
            f1 = 1.1
            newr = min(int(r * f1), 255)
            newg = min(int(g * f1), 255)
            newb = min(int(b * f1), 255)
            col = (newr, newg, newb)

            # Set the color of the border
            f2 = 0.9
            newr = min(int(r * f2), 255)
            newg = min(int(g * f2), 255)
            newb = min(int(b * f2), 255)
            col2 = (newr, newg, newb)

            # Display the rectangle
            self.requireY = y-self.height*0.51
            self.requireHeight = self.height*0.46
            if len(l)==1:
                self.requireX = x-(len(l)+1)*sizeImg-16
                self.requireWidth = (len(l)+1)*sizeImg
                r = pygame.Rect(self.requireX, self.requireY, self.requireWidth, self.requireHeight)
            else:
                self.requireX = x-(len(l)+1)*sizeImg
                self.requireWidth = (len(l)+1)*sizeImg-15
                r = pygame.Rect(self.requireX, self.requireY, self.requireWidth, self.requireHeight)
            pygame.draw.rect(self.screen, col, r, border_radius=10)
            pygame.draw.rect(self.screen, col2, r, 2, border_radius=10)

            # Display the stones
            addOn = -8 if len(l)==1 else 0
            i = 1
            for img_stone in Stones.stonesToImage(l, sizeImg):
                self.screen.blit(img_stone, (x-sizeImg*i-25+addOn, y-self.height*0.49))
                i += 1

            self.displayPointsWithRequire(self.requireX, self.requireY, self.requireWidth, self.requireHeight)
        else:
            self.displayPointsWithoutRequire(x, y)
        

    ## Display the condition of the quest
    def conditionDisplay(self, x:int, y:int) -> None:

        # Set the images and text to display depending of the condition mode
        if self.quest.points != 0:
            
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
    
    def displayNightCondition(self, x, y):
        # Load and display the night image
        img_day = pygame.image.load("./data/img/night.png")
        img_day = pygame.transform.scale(img_day, (60, 60))
        self.screen.blit(img_day, (x-self.width*0.67, y-self.height*0.22))

    def displayMapCondition(self, x, y):
        # Load and display the map image
        img_map = pygame.image.load("./data/img/map.png")
        img_map = pygame.transform.scale(img_map, (60, 60))
        self.screen.blit(img_map, (x-self.width*0.67, y-self.height*0.22))
    
    def displayStoneCondition(self, x, y):
        # Load and display the image of the stone within the condition
        stoneImages = Stones.stonesToImage(self.quest.condition, 50)
        self.screen.blit(stoneImages[0], (x-self.width*0.65, y-self.height*0.2))

    def displayColorCondition(self, x, y):
        i=0
        max = len(self.quest.condition) # The number of color to display
        imgSize = 40
        colorImages = Colors.colorsToImage(self.quest.condition, imgSize)

        # Display the image for all color within the condition 
        for color in colorImages:
            if i==0:
                self.screen.blit(color, (x-self.width*0.63, y-self.height*0.19))
            else:
                self.screen.blit(color, (x-self.width*0.63-(i*imgSize)-20, y-self.height*0.19)) 
            i+=1
            
            # Separate the next image representing a color
            if i != max:
                tmpPol = pygame.font.Font(None, self.policeSize + 45)
                texte_surface = tmpPol.render("/", True, (0,0,0))
                r = texte_surface.get_rect()
                r.center = (x-self.width*0.63-i*10, y-self.height*0.13)
                self.screen.blit(texte_surface, r)
    
    def displaySomeColorCondition(self, x, y):
        # Display all colors
        i=0
        ImgSize = 40
        colorImages = Colors.colorsToImage(self.quest.condition, ImgSize)
        for color in colorImages:
            if i%2==0:
                self.screen.blit(color, (x-self.width*0.63-i*22, y-self.height*0.13))
            else:
                self.screen.blit(color, (x-self.width*0.63-(i-1)*22, y-self.height*0.13-43))
            i+=1

    def displayEqual(self, x, y):
        # If there is any condition display the equal
        if self.quest.conditionMode != ConditionModes.NOTHING: 
            text_eg = self.police.render("=", True, (0,0,0))
            self.screen.blit(text_eg, (x-self.width*0.47, self.pointsCoords[1]+(self.pointsSize[1]/6)))
    
    def displayPointsWithRequire(self, x, y, width, height):
        # Setup the image for the background of the points and display it
        img_pt = pygame.image.load("./data/img/points.png")
        img_pt = pygame.transform.scale(img_pt, self.pointsSize)
        spaceX = (width-self.pointsSize[0])//2
        spaceY = 0.58*height
        self.pointsCoords = (x + spaceX, y + spaceY)
        self.screen.blit(img_pt, self.pointsCoords)

        # Display the points
        texte_surface = self.police.render(str(self.quest.points), True, (0,0,0))
        r = texte_surface.get_rect()
        spaceBetween = 30
        r.center = (x + spaceX + spaceBetween, y + spaceY + spaceBetween) 
        self.screen.blit(texte_surface, r)

    def displayPointsWithoutRequire(self, x, y):
        # Setup the image for the background of the points and display it
        img_pt = pygame.image.load("./data/img/points.png")
        img_pt = pygame.transform.scale(img_pt, self.pointsSize)
        self.pointsCoords = (x-self.width*0.375, y-self.height*0.22)
        self.screen.blit(img_pt, self.pointsCoords)

        # Display the points
        texte_surface = self.police.render(str(self.quest.points), True, (0,0,0))
        r = texte_surface.get_rect()
        r.center = (x-self.width*0.29, y-self.height*0.13)
        self.screen.blit(texte_surface, r)