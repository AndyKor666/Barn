import unittest
from Models.model import GameModel
from Models.mission_model import MissionModel
from Controllers.mission_controller import MissionController

class TestMissionController(unittest.TestCase):

    def setUp(self):
        self.model = GameModel()
        self.mm = MissionModel()
        self.messages = []

        def fake_message(msg):
            self.messages.append(msg)

        self.mc = MissionController(self.model, self.mm, fake_message, lambda: None)

    def test_check_missions_no_crash(self):
        self.mc.check_missions()
        self.assertTrue(True)
