from enum import Enum
import pygame

class Stones(Enum):
    SAPHYR = 1
    RUBY = 2
    EMERALD = 3
    imageSize = 60
    
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
            return "Unknown"
    
    @classmethod
    def stonesToImage(self, stones):
        images = []
        size = (60, 60)
        for s in stones:
            if s == Stones.EMERALD:
                img = pygame.image.load("./data/img/emerald.png")
                img = pygame.transform.scale(img, size)
                images.append(img)
            elif s == Stones.RUBY:
                img = pygame.image.load("./data/img/ruby.png")
                img = pygame.transform.scale(img, size)
                images.append(img)
            elif s == Stones.SAPHYR:
                img = pygame.image.load("./data/img/sapphire.png")
                img = pygame.transform.scale(img, size)
                images.append(img)
        return images

