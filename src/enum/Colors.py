from enum import Enum

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
