import unittest
from Models.model import GameModel

class TestGameModelPlots(unittest.TestCase):

    def setUp(self):
        self.model = GameModel()

    def test_plant_crop(self):
        ok, _ = self.model.plant_crop(0, 1)
        self.assertTrue(ok)
        self.assertEqual(self.model.plots[0].state, "growing")

    def test_harvest(self):
        self.model.plant_crop(0, 1)
        for _ in range(100):
            self.model.tick()

        ok, _ = self.model.harvest(0)
        self.assertTrue(ok)
        self.assertEqual(self.model.stats["plants_harvested"], 1)
