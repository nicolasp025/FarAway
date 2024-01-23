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