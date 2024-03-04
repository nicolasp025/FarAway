from enum import Enum
import pygame

# Enum for the colors of the game
class Colors(Enum):
    GRAY = 0
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    
    ## Get the color from a string representing a color
    @classmethod
    def castToColor(cls, color_str:str) -> Enum:
        for color in cls:
            if color.name == color_str:
                return color
        raise ValueError()

    ## Get the string representation of the color
    @classmethod
    def toString(self, cls:Enum) -> str:
        if cls == Colors.GRAY:
            return "Gray"
        elif cls == Colors.RED:
            return "Red"
        elif cls == Colors.BLUE:
            return "Blue"
        elif cls == Colors.GREEN:
            return "Green"
        elif cls == Colors.YELLOW:
            return "Yellow"
        else:
            raise ValueError("Invalid color.")


    ## Get the string representation of the color in lower case
    @classmethod
    def toStringLower(self, cls:Enum) -> str:
        if cls == Colors.GRAY:
            return "gray"
        elif cls == Colors.RED:
            return "red"
        elif cls == Colors.BLUE:
            return "blue"
        elif cls == Colors.GREEN:
            return "green"
        elif cls == Colors.YELLOW:
            return "yellow"
        else:
            raise ValueError("Invalid color.")

    ## Get the image corresponding to the color
    @classmethod
    def colorToImage(self, color:Enum, size:int) -> pygame.Surface:
        imgSize = (size, size)
        img = pygame.image.load("./data/img/"+Colors.toStringLower(color)+".png")
        img = pygame.transform.scale(img, imgSize)
        return img
    
    ## Get the images corresponding to the colors
    @classmethod
    def colorsToImage(self, c:list[Enum], size:int) -> list[pygame.Surface]:
        return [Colors.colorToImage(i, size) for i in c]
