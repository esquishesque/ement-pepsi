import unittest
from game import *


class TestExecuteHarvest(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_exactlyEnoughFood_harvest_zeroFood(self):
        self.game.playerList[0].stores[supplies["food"]] = 5
        self.game.playerList[0].members = 3
        self.game.playerList[0].babies = 1
        self.game.executeHarvest()
        self.assertEqual(self.game.playerList[0].stores[supplies["food"]],0)

    def test_oneBaby_harvest_zeroBabiesNewAdult(self):
        self.game.playerList[0].members = 1
        self.game.playerList[0].babies = 1
        self.game.executeHarvest()
        self.assertEqual(self.game.playerList[0].members,2)

    def test_twoFoodShort_harvest_twoBeggingCards(self):
        self.game.playerList[0].stores[supplies["food"]] = 0
        self.game.playerList[0].members = 1
        self.game.playerList[0].babies = 0
        self.game.executeHarvest()
        self.assertEqual(self.game.playerList[0].beggingCards,2)

    def test_oneSheepTwoCowsFourPigs_harvest_oneSheepThreeCowsFivePigs(self):
        self.game.playerList[0].stores[supplies["sheeps"]] = 1
        self.game.playerList[0].stores[supplies["cows"]] = 2
        self.game.playerList[0].stores[supplies["pigs"]] = 4
        self.game.executeHarvest()
        self.assertEqual(self.game.playerList[0].stores[supplies["sheeps"]],1)
        self.assertEqual(self.game.playerList[0].stores[supplies["cows"]],3)
        self.assertEqual(self.game.playerList[0].stores[supplies["pigs"]],5)

if __name__ == '__main__':
    unittest.main()


