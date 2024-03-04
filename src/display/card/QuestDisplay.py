import pygame
import sys

sys.path.append("./src/enum/")
from ConditionModes import ConditionModes
from Colors import Colors
from Stones import Stones
from Quest import Quest

## The class to represent the display of a quest card
class QuestDisplay():

    def __init__(self, quest, screen, cardWidth:int, cardHeight:int):
        self.quest = quest
        self.screen = screen
        self.width = cardWidth
        self.height = cardHeight
        
    ## Display the quest
    def display(self, x:int, y:int, color:tuple[int, int, int]) -> None:
        # Display that depends of the type of the card
        self.requireDisplay(x+self.width, y+self.height, color)
        self.conditionDisplay(x+self.width, y+self.height)

        

