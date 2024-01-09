from Colors import *
from Card import *

import random

class RegionCard(Card):
    
    def __init__(self,id):
        self.id = id
        
        self.color = random.choice(list(Colors))