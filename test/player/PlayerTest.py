import unittest
import sys

sys.path.append("./src/player")
sys.path.append("./src/card")

from Player import Player
from RegionCard import RegionCard
from SanctuaryCard import SanctuaryCard

class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.id = 0
        self.player = Player(self.id)

    def test_initialization(self):
        self.assertEqual(self.id, self.player.id)
        self.assertEqual([], self.player.hand)
        self.assertEqual([], self.player.revealedCards)
        self.assertEqual([], self.player.sanctuaryCards)

    def test_addCardToHandWentRight(self):
        card1 = RegionCard(self.id)
        card2 = RegionCard(self.id+1)
        self.player.addCardToHand(card1)
        self.assertEqual(card1, self.player.hand[-1])
        self.player.addCardToHand(card2)
        self.assertEqual(card1, self.player.hand[-2])
        self.assertEqual(card2, self.player.hand[-1])

    def test_addCardToHandWentNotRight(self):
        card1 = RegionCard(self.id)
        card2 = RegionCard(self.id+1)
        card3 = RegionCard(self.id+2)
        card4 = RegionCard(self.id+3)
        cardS = SanctuaryCard(self.id)
        self.player.addCardToHand(cardS)
        self.assertEqual(0, len(self.player.hand))
        self.player.addCardToHand(card1)
        self.player.addCardToHand(card2)
        self.player.addCardToHand(card3)
        self.player.addCardToHand(card4)
        self.assertEqual(3, len(self.player.hand))


    def test_addSanctuaryCardWentRight(self):
        card1 = SanctuaryCard(self.id)
        card2 = SanctuaryCard(self.id+1)
        self.player.addCardToSanctuaryCards(card1)
        self.assertEqual(card1, self.player.sanctuaryCards[-1])
        self.player.addCardToSanctuaryCards(card2)
        self.assertEqual(card1, self.player.sanctuaryCards[-2])
        self.assertEqual(card2, self.player.sanctuaryCards[-1])

    def test_addSanctuaryCardWentNotRight(self):
        card = RegionCard(self.id)
        self.player.addCardToSanctuaryCards(card)
        self.assertEqual(0, len(self.player.sanctuaryCards))

    def test_revealingACardWentRight(self):
        card = RegionCard(self.id)
        self.player.addCardToHand(card)
        res = self.player.revealCard(1)
        self.assertEqual(self.id, res)
        self.assertEqual(card, self.player.revealedCards[-1])

    def test_revealingACardDidntWentRight(self):
        card = RegionCard(self.id)
        self.player.addCardToHand(card)
        res = self.player.revealCard(0)
        self.assertEqual(None, res)
        self.assertEqual(0, len(self.player.revealedCards))

    def test_canRevealACard(self):
        self.assertEqual(False, self.player.canRevealCard())
        card = RegionCard(self.id)
        self.player.addCardToHand(card)
        self.assertEqual(True, self.player.canRevealCard())
        self.player.revealCard(1)
        self.assertEqual(False, self.player.canRevealCard())




if __name__ == "__main__":
    unittest.main()

