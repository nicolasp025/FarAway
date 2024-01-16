
class Quest:

    def __init__(self, require, points, conditionMode, condition):
        self.require = require
        self.points = points
        self.conditionMode = conditionMode
        self.condition = condition

    def toString(self):
        return "Quest require : " + str(self.require) + " for " + str(self.points) + " points with condition mode : " + str(self.conditionMode) + " you need the condition : " + str(self.condition) + "\n"