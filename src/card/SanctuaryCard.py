import sys
sys.path.append("./src/enum")
sys.path.append("./src/enum")
from Colors import *
from Card import *

## The class which represents the sanctuary cards
class SanctuaryCard(Card):
    
    def __init__(self, id, color=None, quest=None, stones=[], day=False, map=False):
        super().__init__(id, color, quest, stones, day, map)


    def toString(self) -> str:
        return "SanctuaryCard"+super().toString()