from enum import Enum
import pygame

## Enum for the stones of the game
class Stones(Enum):
    SAPPHIRE = 1
    RUBY = 2
    EMERALD = 3
    
    ## Get the stone from a string representing a stone
    @classmethod
    def castToStone(cls, stone_str:str) -> Enum:
        for stone in cls:
            if stone.name == stone_str:
                return stone
        raise ValueError()
    
    ## Get the string representation of the stone
    @classmethod
    def toString(self, stone:Enum) -> str:
        tmp = {
            Stones.SAPPHIRE: "Sapphire",
            Stones.RUBY: "Ruby",
            Stones.EMERALD: "Emerald"
        }
        if stone in tmp:
            return tmp[stone]
        else:
            raise ValueError("Invalid color.")
    
    ## Get the string representation of the stone in lower case
    @classmethod
    def toStringLower(self, stone:Enum) -> str:
        tmp = {
            Stones.SAPPHIRE: "sapphire",
            Stones.RUBY: "ruby",
            Stones.EMERALD: "emerald"
        }
        if stone in tmp:
            return tmp[stone]
        else:
            raise ValueError("Invalid color.")

    ## Get the images corresponding to the stones
    @classmethod
    def stonesToImage(self, stones:list[Enum], size:int) -> list[pygame.Surface]:
        return [Stones.stoneToImage(i, size) for i in stones]

    ## Get the image corresponding to the stone
    @classmethod
    def stoneToImage(self, stone:Enum, size:int) -> pygame.Surface:
        imgSize = (size, size)
        img = pygame.image.load("./data/img/"+Stones.toStringLower(stone)+".png")
        img = pygame.transform.scale(img, imgSize)
        return img