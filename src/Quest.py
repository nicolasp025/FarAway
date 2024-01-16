
class Quest:

    def __init__(self, listStones, points, conditionMode, condition):
        self.listStones = listStones
        self.points = points
        self.conditionMode = conditionMode
        self.condition = condition

    def toString(self):
        return "Quest require : " + str(self.listStones) + " for " + str(self.points) + " points with condition mode : " + str(self.conditionMode) + " you need the condition : " + str(self.condition) + "\n"