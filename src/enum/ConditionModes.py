from enum import Enum

# Enum for the condition modes of the game
class ConditionModes(Enum):
    # Do not use 0
    NOTHING = 1
    NIGHT = 2
    MAP = 3
    STONE = 4
    COLOR = 5
    SOMECOLOR = 6
    
    ## Get the condition mode from a string representing a condition mode
    @classmethod
    def castToMode(cls, x:str) -> Enum:
        for mode in cls:
            if mode.name == x:
                return mode
        raise ValueError()
    