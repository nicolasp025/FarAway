from Colors import *
from Card import *

import random

class RegionCard(Card):
    
    def __init__(self, number, color=None, quest=None, stones=[], day=False, map=False):
        super().__init__(number, color, quest, stones, day, map)
        self.id = number
        self.color = random.choice(list(Colors))


    def toString(self):
        print("RegionCard : " + str(self.id) + "\n")