import unittest
import sys

sys.path.append("./src/game/")

from Board import Board


class RegionCardTest(unittest.TestCase):
    
    def setUp(self):
        self.id = 0
        self.card = Card(self.id)

    def test_initializationWentRight(self):
        self.assertEqual(self.id, self.card.id)
        self.assertEqual(None, self.card.color)
        self.assertEqual(None, self.card.quest)
        self.assertEqual([], self.card.stones)
        self.assertEqual(False, self.card.map)
        self.assertEqual(False, self.card.day)


if __name__ == "__main__":
    unittest.main()