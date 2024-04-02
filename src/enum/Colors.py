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
        tmp = {
            Colors.GRAY: "Gray",
            Colors.RED: "Red",
            Colors.BLUE: "Blue",
            Colors.GREEN: "Green",
            Colors.YELLOW: "Yellow"
        }
        if cls in tmp:
            return tmp[cls]
        else:
            raise ValueError("Invalid color.")


    ## Get the string representation of the color in lower case
    @classmethod
    def toStringLower(self, cls:Enum) -> str:
        tmp = {
            Colors.GRAY: "gray",
            Colors.RED: "red",
            Colors.BLUE: "blue",
            Colors.GREEN: "green",
            Colors.YELLOW: "yellow"
        }
        if cls in tmp:
            return tmp[cls]
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
