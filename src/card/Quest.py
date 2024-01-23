import sys 
sys.path.append("./src/enum/")

from ConditionModes import ConditionModes


class Quest:

    def __init__(self, require, points, conditionMode, condition):
        self.require = require
        self.points = points
        self.conditionMode = conditionMode
        self.condition = condition

    def toString(self):
        res = ""
        if self.points != "0":
            res += "quest : "
            res += "require " + str(self.require)
            if self.conditionMode == "NOTHING":
                res +=", gain " + self.points + " points"
            else:
              res += ", gain " + self.points + " points"
              if self.conditionMode == "NIGHT":
                res += " for each night card"
              elif self.conditionMode == "MAP":
                res += " for each map"
              elif self.conditionMode == "STONE":
                res += " for each " + self.condition[0]
              elif self.conditionMode == "COLOR":
                res += " for each card with a color within " + str(self.condition)
              else:
                res += " for each combo of cards of all colors in " + str(self.condition)
        else:
           res += "no quest"
        return res