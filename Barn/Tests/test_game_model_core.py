import unittest
from Models.model import GameModel


class TestGameModelCore(unittest.TestCase):
    def setUp(self):
        self.model = GameModel()

    def test_initial_state(self):
        self.assertIsInstance(self.model.balance, int)
        self.assertGreaterEqual(self.model.balance, 0)
        self.assertEqual(len(self.model.plots), 3)
        self.assertIn("plants_planted", self.model.stats)
        self.assertIn("plants_harvested", self.model.stats)

    def test_get_plant_by_id_found(self):
        plant = self.model.get_plant_by_id(1)
        self.assertIsNotNone(plant)

    def test_get_plant_by_id_not_found(self):
        plant = self.model.get_plant_by_id(9999)
        self.assertIsNone(plant)

    def test_get_fertilizer_by_id_found(self):
        fert = self.model.get_fertilizer_by_id(1)
        self.assertIsNotNone(fert)

    def test_get_fertilizer_by_id_not_found(self):
        fert = self.model.get_fertilizer_by_id(9999)
        self.assertIsNone(fert)
