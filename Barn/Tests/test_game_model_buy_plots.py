import unittest
from Models.model import GameModel

class TestGameModelBuyPlots(unittest.TestCase):
    def setUp(self):
        self.model = GameModel()

    def test_buy_new_plot_not_enough_money(self):
        self.model.balance = 100
        old_len = len(self.model.plots)

        ok, msg = self.model.buy_new_plot(None)

        self.assertFalse(ok)
        self.assertIn("not enough", msg.lower())
        self.assertEqual(len(self.model.plots), old_len)
        self.assertEqual(self.model.stats["plots_bought"], 0)

    def test_buy_new_plot_success(self):
        self.model.balance = 5000
        old_len = len(self.model.plots)

        ok, msg = self.model.buy_new_plot(None)

        self.assertTrue(ok)
        self.assertIn("bought", msg.lower())
        self.assertEqual(len(self.model.plots), old_len + 1)
        self.assertEqual(self.model.stats["plots_bought"], 1)

    def test_buy_new_plot_max_plots_block(self):
        self.model.balance = 10**9
        while len(self.model.plots) < self.model.MAX_PLOTS:
            ok, _ = self.model.buy_new_plot(None)
            self.assertTrue(ok)

        ok, msg = self.model.buy_new_plot(None)
        self.assertFalse(ok)
        self.assertIn("maximum", msg.lower())
