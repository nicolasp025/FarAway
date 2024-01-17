import sys
sys.path.append("/home/nathsign/Documents/COURS/L3/S6/PROJET/projet-far-away/src/enum")


from Colors import *


class Card:
    
    def __init__(self, id, color=None, quest=None, stones=[], day=False, map=False):
        self.id = id
        self.color = color
        self.quest = quest
        self.stones = stones
        self.day = day
        self.map = map
        
