import sys
sys.path.append("../enum")
sys.path.append("../card")
from Colors import Colors
from Card import Card

import random

class RegionCard(Card):
    
    def __init__(self, number, color=None, quest=None, stones=[], day=False, map=False):
        super().__init__(number, color, quest, stones, day, map)
        self.id = number
        self.color = random.choice(list(Colors))


    def toString(self):
        return "Region"+super().toString()