from enum import Enum
import pygame

class Colors(Enum):
    GRAY = 0
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    
    @classmethod
    def castToColor(cls, color_str):
        for color in cls:
            if color.name == color_str:
                return color
        raise ValueError()

    @classmethod
    def toString(self, cls):
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

    @classmethod
    def toStringLower(self, cls):
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

    @classmethod
    def colorToImage(self, color, size):
        imgSize = (size, size)
        img = pygame.image.load("./data/img/"+Colors.toStringLower(color)+".png")
        img = pygame.transform.scale(img, imgSize)
        return img
    
    @classmethod
    def colorsToImage(self, c, size):
        return [Colors.colorToImage(i, size) for i in c]
