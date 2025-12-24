import unittest
from Models.model import GameModel

class TestGameModel(unittest.TestCase):

    def setUp(self):
        self.model = GameModel()

    def test_initial_balance(self):
        self.assertEqual(self.model.balance, 50)

    def test_buy_fertilizer_success(self):
        ok, _ = self.model.buy_fertilizer(1)
        self.assertTrue(ok)
        self.assertEqual(self.model.fertilizer_inventory[1], 1)

    def test_buy_fertilizer_not_enough_money(self):
        self.model.balance = 0
        ok, msg = self.model.buy_fertilizer(1)
        self.assertFalse(ok)
        self.assertEqual(msg, "Not enough money :(")

    def test_sell_crop_increases_balance(self):
        self.model.barn["Corn"] = 1
        old_balance = self.model.balance
        self.model.sell_from_barn("Corn")
        self.assertGreater(self.model.balance, old_balance)
