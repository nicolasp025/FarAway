import sys
sys.path.append("./src/enum")
sys.path.append("./src/enum")
from Colors import *
from Card import *


class SanctuaryCard(Card):
    
    def __init__(self, id, color=None, quest=None, stones=[], day=False, map=False):
        super().__init__(id, color, quest, stones, day, map)


    def toString(self):
        return "SanctuaryCard"+super().toString()