<<<<<<< HEAD
from enum import *
=======
from enum import Enum
>>>>>>> c090fe1 (update des enum pour cast)

class Stones(Enum):
    SAPHYR = 1
    RUBY = 2
    EMERALD = 3
    
    @classmethod
    def castToStone(cls, color_str):
        for color in cls:
            if color.name == color_str:
                return color
        raise ValueError()