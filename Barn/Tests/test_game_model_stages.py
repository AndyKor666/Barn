import unittest
from Models.model import GameModel


class TestGameModelStages(unittest.TestCase):
    def setUp(self):
        self.model = GameModel()

    def test_get_plot_stage_index_ready_returns_max_stage(self):
        ok, el = self.model.plant_crop(0, 1)
        self.assertTrue(ok)
        for el in range(5000):
            self.model.tick()
            if self.model.plots[0].state == "ready":
                break

        plot = self.model.plots[0]
        stage = self.model.get_plot_stage_index(plot)

        self.assertEqual(stage, plot.plant.stages)

    def test_get_plot_stage_index_growing_in_range(self):
        ok, el = self.model.plant_crop(0, 1)
        self.assertTrue(ok)

        plot = self.model.plots[0]
        for el in range(3):
            self.model.tick()

        stage = self.model.get_plot_stage_index(plot)
        self.assertGreaterEqual(stage, 1)
        self.assertLessEqual(stage, plot.plant.stages)
