import unittest
from Models.model import GameModel


class TestGameModelSellShop(unittest.TestCase):
    def setUp(self):
        self.model = GameModel()

    def test_sell_from_barn_increases_balance_and_income_stat(self):
        self.model.barn["Corn"] = 1
        old_balance = self.model.balance
        old_income = self.model.stats["sold_income"]

        ok, msg = self.model.sell_from_barn("Corn")

        self.assertTrue(ok)
        self.assertIn("Sold", msg)
        self.assertGreater(self.model.balance, old_balance)
        self.assertGreater(self.model.stats["sold_income"], old_income)

    def test_sell_from_barn_decreases_barn_count(self):
        self.model.barn["Corn"] = 2
        ok, _ = self.model.sell_from_barn("Corn")

        self.assertTrue(ok)
        self.assertEqual(self.model.barn["Corn"], 1)
