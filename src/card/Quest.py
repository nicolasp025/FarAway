import sys 
sys.path.append("./src/enum/")

from ConditionModes import ConditionModes
from Stones import Stones
from Colors import Colors


class Quest:

    def __init__(self, require, points, conditionMode, condition):
        tmpRequire = {}
        for i in require:
          if i not in tmpRequire:
            tmpRequire[i] = 1
          else:
            tmpRequire[i] += 1
        
        self.require = tmpRequire
        self.points = points
        self.conditionMode = conditionMode
        self.condition = condition

    def satisfy(self, ressources):
      ## Returns the number of points won by this card
      for stone in self.require:
          if stone not in ressources or self.require[stone]>ressources[stone]:
            return 0
      
      if self.conditionMode == ConditionModes.NOTHING:
        return self.points
      elif self.conditionMode == ConditionModes.NIGHT:
        return self.points * ressources["night"]
      elif self.conditionMode == ConditionModes.MAP:
        return self.points * ressources["map"]
      elif self.conditionMode == ConditionModes.STONE or self.conditionMode == ConditionModes.COLOR:
        tmpRes = 0
        for i in self.condition:
          tmpRes += ressources[i] * self.points 
        return tmpRes
      elif self.conditionMode == ConditionModes.SOMECOLOR:
        for color in self.condition:
          if color not in ressources: 
            return 0                                            # If one color is missing then return 0 pts
        return min([ressources[i] for i in self.condition]) * self.points
          
    def toString(self):
        res = ""
        if self.points != 0:
            res += "quest : require "
            l = list(self.require.items())
            if len(l) == 0:
              res += "nothing"
            else:
              res += " and ".join(list(map(lambda x : str(x[1]) + " " + Stones.toString(x[0]), l)))
            res +=", gain " + str(self.points) + " points"
            if self.conditionMode == ConditionModes.NOTHING:
              res += "."
            elif self.conditionMode == ConditionModes.NIGHT:
              res += " for each night card."
            elif self.conditionMode == ConditionModes.MAP:
              res += " for each map."
            elif self.conditionMode == ConditionModes.STONE:
              res += " for each " + " | ".join(list(map(lambda x : Stones.toString(x), self.condition)))+ "."
            elif self.conditionMode == ConditionModes.COLOR:
              res += " for each card with a color " + " or ".join(list(map(lambda x: Colors.toString(x), self.condition))) + "."
            elif self.conditionMode == ConditionModes.SOMECOLOR:
              res += " for each combo of cards of all colors in " + " | ".join(list(map(lambda x : Colors.toString(x), self.condition))) + "."
        else:
           res += "no quest."
        return res