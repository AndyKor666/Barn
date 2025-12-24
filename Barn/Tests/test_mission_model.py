import unittest
from Models.mission_model import MissionModel
from Models.mission import Mission
from Models.model import GameModel

class TestMissionModel(unittest.TestCase):

    def setUp(self):
        self.model = GameModel()
        self.mm = MissionModel()

    def test_mission_not_completed(self):
        m = Mission(1, "Test", "Desc", lambda m: m.stats["plants_planted"] >= 1, 10)
        self.mm.add_mission(m)

        completed = self.mm.check(self.model)
        self.assertEqual(len(completed), 0)

    def test_mission_completed(self):
        m = Mission(1, "Test", "Desc", lambda m: m.stats["plants_planted"] >= 1, 10)
        self.mm.add_mission(m)

        self.model.stats["plants_planted"] = 1
        completed = self.mm.check(self.model)

        self.assertEqual(len(completed), 1)
        self.assertTrue(m.completed)
