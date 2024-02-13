import pygame
import sys

sys.path.append("./src/enum/")
from ConditionModes import ConditionModes
from Colors import Colors
from Stones import Stones
from Quest import Quest


class QuestDisplay():

    def __init__(self, quest, screen, cardWidth, cardHeight):
        self.quest = quest
        self.screen = screen
        self.width = cardWidth
        self.height = cardHeight
        
    def display(self, x, y):
        self.conditionDisplay(x+self.width, y+self.height)

        

