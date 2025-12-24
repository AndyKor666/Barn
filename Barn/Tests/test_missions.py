import unittest
from Models.model import GameModel
from Models.mission import Mission
from Models.mission_model import MissionModel


class TestMissionModel(unittest.TestCase):
    def setUp(self):
        self.model = GameModel()
        self.mm = MissionModel()

    def test_check_no_missions_returns_empty(self):
        completed = self.mm.check(self.model)
        self.assertEqual(completed, [])

    def test_mission_not_completed_when_condition_false(self):
        m = Mission(1, "First Sprout", "Plant your first crop",
                    lambda model: model.stats["plants_planted"] >= 1,
                    20)
        self.mm.add_mission(m)

        completed = self.mm.check(self.model)
        self.assertEqual(len(completed), 0)
        self.assertFalse(m.completed)

    def test_mission_completes_when_condition_true(self):
        m = Mission(1, "First Sprout", "Plant your first crop",
                    lambda model: model.stats["plants_planted"] >= 1,
                    20)
        self.mm.add_mission(m)

        self.model.stats["plants_planted"] = 1
        completed = self.mm.check(self.model)

        self.assertEqual(len(completed), 1)
        self.assertTrue(m.completed)
        self.assertEqual(completed[0].id, 1)

    def test_mission_completes_only_once(self):
        m = Mission(1, "First Sprout", "Plant your first crop",
                    lambda model: model.stats["plants_planted"] >= 1,
                    20)
        self.mm.add_mission(m)

        self.model.stats["plants_planted"] = 1
        completed1 = self.mm.check(self.model)
        completed2 = self.mm.check(self.model)

        self.assertEqual(len(completed1), 1)
        self.assertEqual(len(completed2), 0)
