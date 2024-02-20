from enum import Enum
import pygame

class Stones(Enum):
    SAPHYR = 1
    RUBY = 2
    EMERALD = 3
    
    @classmethod
    def castToStone(cls, stone_str):
        for stone in cls:
            if stone.name == stone_str:
                return stone
        raise ValueError()
    
    @classmethod
    def toString(self, stone):
        if stone == Stones.SAPHYR:
            return "Sapphire"
        elif stone == Stones.RUBY:
            return "Ruby"
        elif stone == Stones.EMERALD:
            return "Emerald"
        else:
            raise ValueError("Invalid color.")
    
    @classmethod
    def toStringLower(self, stone):
        if stone == Stones.SAPHYR:
            return "sapphire"
        elif stone == Stones.RUBY:
            return "ruby"
        elif stone == Stones.EMERALD:
            return "emerald"
        else:
            raise ValueError("Invalid color.")

    @classmethod
    def stonesToImage(self, stones, size):
        images = []
        for s in stones:
            images.append(Stones.stoneToImage(s, size))
        return images

    @classmethod
    def stoneToImage(self, stone, size):
        imgSize = (size, size)
        img = pygame.image.load("./data/img/"+Stones.toStringLower(stone)+".png")
        img = pygame.transform.scale(img, imgSize)
        return img