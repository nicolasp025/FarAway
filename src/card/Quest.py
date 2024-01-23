import sys 
sys.path.append("./src/enum/")

from ConditionModes import ConditionModes


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

    def satisfy(ressources):
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
        tmpRes += ressources[i] * self.points for i in self.condition
        return tmpRes
      else : # ConditionMode = SOMECOLOR
        repeater = 1
        conditionRespected = True
        while conditionRespected:
          for color in self.condition:
            
            return 0 # to remove
            # to finish



    def toString(self):
        res = ""
        if self.points != "0":
            res += "quest : "
            res += "require " + str(self.require)
            if self.conditionMode == ConditionModes.NOTHING:
                res +=", gain " + self.points + " points"
            else:
              res += ", gain " + self.points + " points"
              if self.conditionMode == ConditionModes.NIGHT:
                res += " for each night card"
              elif self.conditionMode == ConditionModes.MAP:
                res += " for each map"
              elif self.conditionMode == "STONE":
                res += " for each " + self.condition[0]
              elif self.conditionMode == ConditionModes.COLOR:
                res += " for each card with a color within " + str(self.condition)
              else:
                res += " for each combo of cards of all colors in " + str(self.condition)
        else:
           res += "no quest"
        return res