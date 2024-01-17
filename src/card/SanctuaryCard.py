import sys
sys.path.append("/home/nathsign/Documents/COURS/L3/S6/PROJET/projet-far-away/src/enum")
sys.path.append("/home/nathsign/Documents/COURS/L3/S6/PROJET/projet-far-away/src/enum")
from Colors import *
from Card import *


class SanctuaryCard(Card):
    
    def __init__(self, id, color=None, quest=None, stones=[], day=False, map=False):
        super().__init__(id, color, quest, stones, day, map)


    def toString(self):
        print("SanctuaryCard id : " + str(self.id) + " | quest : " + self.quest.toString() + " | stones : " + str(self.stones) + " | day : " + str(self.day) + " | map : " + str(self.map) + "\n")