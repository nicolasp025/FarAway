import sys
sys.path.append("./src/enum")
sys.path.append("./src/card")
from Colors import Colors
from Card import Card

## The class which represents the region cards
class RegionCard(Card):
    
    def __init__(self, number, color=None, quest=None, stones=[], day=False, map=False):
        super().__init__(number, color, quest, stones, day, map)


    def toString(self) -> str:
        return "RegionCard number "+str(self.id)+super().toString()