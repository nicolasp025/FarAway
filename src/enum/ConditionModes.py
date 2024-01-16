from enum import Enum

class ConditionModes(Enum):
    # Do not use 0
    NOTHING = 1
    NIGHT = 2
    MAP = 3
    STONE = 4
    COLOR = 5
    SOMECOLOR = 6
    