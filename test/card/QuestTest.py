import unittest
import sys

sys.path.append("./src/card")
sys.path.append("./src/enum/")

from Quest import Quest
from ConditionModes import ConditionModes
from Colors import Colors
from Stones import Stones

class QuestTest(unittest.TestCase):

    def test_Mode_Nothing_Require_Respected(self):
        quest = Quest([], 1, ConditionModes.NOTHING, [])
        ressources = {}
        self.assertEqual(quest.satisfy(ressources), 1)

    def test_Mode_Nothing_Require_NotRespected(self):
        quest = Quest([Stones.RUBY, Stones.RUBY], 1, ConditionModes.NOTHING, [])
        ressources = {Stones.RUBY: 1}
        self.assertEqual(quest.satisfy(ressources), 0)

    def test_Mode_Night_Require_Respected(self):
        quest = Quest([Stones.RUBY, Stones.RUBY], 1, ConditionModes.NIGHT, [])
        ressources = {Stones.RUBY: 2, "night": 2}
        self.assertEqual(quest.satisfy(ressources), 2)
    
    def test_Mode_Night_Require_NotRespected(self):
        quest = Quest([Stones.RUBY, Stones.RUBY], 1, ConditionModes.NIGHT, [])
        ressources = {Stones.RUBY: 1, "night": 2}
        self.assertEqual(quest.satisfy(ressources), 0)

    def test_Mode_Map_Require_Respected(self):
        quest = Quest([Stones.RUBY, Stones.RUBY], 1, ConditionModes.MAP, [])
        ressources = {Stones.RUBY: 2, "map": 2}
        self.assertEqual(quest.satisfy(ressources), 2)

    def test_Mode_Map_Require_NotRespected(self):
        quest = Quest([Stones.RUBY, Stones.RUBY], 1, ConditionModes.MAP, [])
        ressources = {Stones.RUBY: 1, "map": 2}
        self.assertEqual(quest.satisfy(ressources), 0)

    def test_Mode_Stone_Require_Respected(self):
        quest = Quest([Stones.RUBY, Stones.RUBY], 1, ConditionModes.STONE, [Stones.RUBY])
        ressources = {Stones.RUBY: 2}
        self.assertEqual(quest.satisfy(ressources), 2)

    def test_Mode_Stone_Require_NotRespected(self):
        quest = Quest([Stones.RUBY, Stones.RUBY], 1, ConditionModes.STONE, [Stones.RUBY])
        ressources = {Stones.RUBY: 1}
        self.assertEqual(quest.satisfy(ressources), 0)

    def test_Mode_Color_Require_Respected(self):
        quest = Quest([Stones.RUBY, Stones.RUBY], 1, ConditionModes.COLOR, [Colors.RED])
        ressources = {Stones.RUBY: 2, Colors.RED: 10}
        self.assertEqual(quest.satisfy(ressources), 10)

    def test_Mode_Stone_Require_NotRespected(self):
        quest = Quest([Stones.RUBY, Stones.RUBY], 1, ConditionModes.COLOR, [Colors.RED])
        ressources = {Stones.RUBY: 1, Colors.RED: 1}
        self.assertEqual(quest.satisfy(ressources), 0)

    def test_Mode_SomeColor_Require_Respected(self):
        quest = Quest([Stones.RUBY, Stones.RUBY], 10, ConditionModes.SOMECOLOR, [Colors.RED, Colors.GREEN, Colors.YELLOW, Colors.BLUE])
        ressources = {Stones.RUBY: 2, Colors.RED: 2, Colors.BLUE: 3, Colors.GREEN: 2, Colors.YELLOW: 4}
        self.assertEqual(quest.satisfy(ressources), 20)

    def test_Mode_SomeColor_Require_NotRespected(self):
        quest = Quest([Stones.RUBY, Stones.RUBY], 10, ConditionModes.SOMECOLOR, [Colors.RED, Colors.GREEN, Colors.YELLOW, Colors.BLUE])
        ressources = {Stones.RUBY: 1, Colors.RED: 2, Colors.BLUE: 3, Colors.GREEN: 2, Colors.YELLOW: 4}
        self.assertEqual(quest.satisfy(ressources), 0)
    
if __name__ == "__main__":
    unittest.main()