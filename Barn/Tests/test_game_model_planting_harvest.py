import unittest
from Models.model import GameModel


class TestGameModelPlantingHarvest(unittest.TestCase):
    def setUp(self):
        self.model = GameModel()

    def _fast_forward_until_ready(self, plot_index=0, max_ticks=5000):
        for el in range(max_ticks):
            self.model.tick()
            if self.model.plots[plot_index].state == "ready":
                return True
        return False

    def test_plant_crop_success_changes_plot_and_stats(self):
        ok, msg = self.model.plant_crop(0, 1)
        self.assertTrue(ok)
        self.assertIn("Planted", msg)

        self.assertEqual(self.model.plots[0].state, "growing")
        self.assertEqual(self.model.stats["plants_planted"], 1)

    def test_tick_eventually_makes_ready(self):
        ok, el = self.model.plant_crop(0, 1)
        self.assertTrue(ok)

        became_ready = self._fast_forward_until_ready(0)
        self.assertTrue(became_ready)
        self.assertEqual(self.model.plots[0].state, "ready")

    def test_harvest_puts_item_to_barn_and_resets_plot(self):
        ok, el = self.model.plant_crop(0, 1)
        self.assertTrue(ok)
        self.assertTrue(self._fast_forward_until_ready(0))

        ok, msg = self.model.harvest(0)
        self.assertTrue(ok)
        self.assertIn("Harvested", msg)

        self.assertGreaterEqual(self.model.barn.get("Corn", 0), 1)
        self.assertEqual(self.model.stats["plants_harvested"], 1)

        plot = self.model.plots[0]
        self.assertEqual(plot.state, "empty")
        self.assertIsNone(plot.plant)
        self.assertEqual(plot.remaining_time, 0)
        self.assertEqual(plot.total_time, 0)
