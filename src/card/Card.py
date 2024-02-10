import sys
sys.path.append("./src/enum")


from Colors import Colors
from Stones import Stones


class Card:
    
    def __init__(self, id, color=None, quest=None, stones=[], day=False, map=False, dcard=None):
        self.id = id
        self.color = color
        self.quest = quest
        self.stones = stones
        self.day = day
        self.map = map
        self.dcard = dcard
        
    def toString(self):
        res = ", color : " + Colors.toString(self.color)
        if len(self.stones) > 0:
            res += ", with stone(s) : " + " | ".join(list(map(lambda x : Stones.toString(x), self.stones)))
        if self.day:
            res += ", day card"
        else:
            res += ", night card" 
        if self.map:
            res += ", contains a map"
        if self.quest != None:
            res += " with " + self.quest.toString()
        res += "\n"
        return res
    
    def addDisplayCard(self, displayCard):
        self.dcard = displayCard
    
    def satisfy(self, ressources):
        return self.quest.satisfy(ressources)
