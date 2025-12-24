import unittest
from Models.model import GameModel

class TestGameModelFertilizer(unittest.TestCase):
    def setUp(self):
        self.model = GameModel()

    def test_buy_fertilizer_success(self):
        self.model.balance = 50
        ok, msg = self.model.buy_fertilizer(1)

        self.assertTrue(ok)
        self.assertIn("bought", msg.lower())
        self.assertEqual(self.model.fertilizer_inventory[1], 1)
        self.assertEqual(self.model.balance, 40)

    def test_buy_fertilizer_not_enough_money(self):
        self.model.balance = 0
        ok, msg = self.model.buy_fertilizer(1)

        self.assertFalse(ok)
        self.assertEqual(msg, "Not enough money :(")
        self.assertEqual(self.model.balance, 0)
        self.assertEqual(self.model.fertilizer_inventory[1], 0)

    def test_plant_with_fertilizer_consumes_inventory_and_updates_stat(self):
        self.model.balance = 50
        ok, _ = self.model.buy_fertilizer(1)
        self.assertTrue(ok)
        self.assertEqual(self.model.fertilizer_inventory[1], 1)

        ok, msg = self.model.plant_crop(0, 1, fertilizer_id=1)
        self.assertTrue(ok)
        self.assertIn("Planted", msg)

        self.assertEqual(self.model.fertilizer_inventory[1], 0)
        self.assertEqual(self.model.stats["fertilizers_used"], 1)

    def test_plant_with_fertilizer_but_none_in_inventory(self):
        ok, msg = self.model.plant_crop(0, 1, fertilizer_id=1)
        self.assertFalse(ok)
        self.assertEqual(msg, "No fertilizer :(")
        self.assertEqual(self.model.plots[0].state, "empty")
