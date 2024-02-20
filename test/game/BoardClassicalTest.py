import unittest
import sys
import io 

sys.path.append("./src/game/")
sys.path.append("./src/player/")

from Player import Player
from BoardClassical import BoardClassical

output = io.StringIO()
sys.stdout = output

class BoardTest(unittest.TestCase):
    
    def setUp(self):
        self.board = BoardClassical()

    def test_numberPlayerWentRight(self):
        n = 3 ## Between 2 and 6
        sys.stdin = io.StringIO(str(n)+"\n")
        self.board.chooseNbPlayers()
        self.assertEqual(n, len(self.board.players))

    def test_numberPlayerDidntWentRight(self):
        n = 7 ## Between 2 and 6, here impossible
        sys.stdin = io.StringIO(str(n)+"\n")
        self.board.chooseNbPlayers()
        self.assertEqual(0, len(self.board.players))
    
    def test_chooseCardToReveal(self):
        n = 3 ## Between 2 and 6
        sys.stdin = io.StringIO(str(n)+"\n")
        self.board.chooseNbPlayers()
        input = "".join(["1\n" for i in range(n+1)])
        sys.stdin = io.StringIO(input)
        self.board.chooseCardToReveal()
        for p in self.board.players:
            self.assertEqual(2, len(p.hand))

    def test_chooseRegionCard(self):
        n = 3 ## Between 2 and 6
        sys.stdin = io.StringIO(str(n)+"\n")
        self.board.chooseNbPlayers()
        for i in range(len(self.board.players)+1):
            self.board.RegionCardRevealed.append(self.board.regionCards.pop(0))
        input = "".join(["1\n" for i in range(n+1)])
        sys.stdin = io.StringIO(input)
        self.board.chooseRegionCard()
        for p in self.board.players:
            self.assertEqual(3, len(p.hand))

    def test_chooseSanctuaryCard(self):
        n = 3 ## Between 2 and 6
        sys.stdin = io.StringIO(str(n)+"\n")
        self.board.chooseNbPlayers()
        for i in range(2):
            for i in range(len(self.board.players)+1):
                self.board.RegionCardRevealed.append(self.board.regionCards.pop(0))
            pl = []
            for p in self.board.players:
                if p.sanctuaryCardToAdd() > 0:
                    pl.append(p)
            input = "".join(["1\n" for i in range(len(pl)+1)])
            sys.stdin = io.StringIO(input)
            self.board.chooseSanctuaryCard()
            for p in pl:
                self.assertEqual(1, len(p.sanctuaryCards))
            input = "".join(["1\n" for i in range(n+1)])
            sys.stdin = io.StringIO(input)
            self.board.chooseRegionCard()
            for p in self.board.players:
                self.assertEqual(3, len(p.hand))
            self.RegionCardRevealed = []

    def test_manyTurns(self):
        n = 6     ## Between 2 and 6
        nbTurns = 8 ## Between 0 and 8
        sys.stdin = io.StringIO(str(n)+"\n")
        self.board.chooseNbPlayers()
        for actualTurn in range(nbTurns):
            input = "".join(["1\n" for i in range(n+1)])
            sys.stdin = io.StringIO(input)
            self.board.chooseCardToReveal()
            pl = []
            for p in self.board.players:
                if p.sanctuaryCardToAdd() > 0:
                    pl.append((p, len(p.sanctuaryCards)))
            input = "".join(["1\n" for i in range(len(pl)+1)])
            sys.stdin = io.StringIO(input)
            self.board.chooseSanctuaryCard()
            for (p, nb) in pl:
                self.assertEqual(nb+1, len(p.sanctuaryCards))
            if actualTurn < 7:
                input = "".join(["1\n" for i in range(n+1)])
                sys.stdin = io.StringIO(input)
                self.board.chooseRegionCard()
                for p in self.board.players:
                    self.assertEqual(3, len(p.hand))
            self.RegionCardRevealed = []


if __name__ == "__main__":
    unittest.main()