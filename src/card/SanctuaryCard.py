import sys
sys.path.append("../enum")
sys.path.append("../enum")
from Colors import *
from Card import *


class SanctuaryCard(Card):
    
    def __init__(self, id, color=None, quest=None, stones=[], day=False, map=False):
        super().__init__(id, color, quest, stones, day, map)


    def toString(self):
        return "Sanctuary"+super().toString()