from enum import Enum

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
            return "Unknown"