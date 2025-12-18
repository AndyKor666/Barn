from Missions.mission import Mission

class MissionModel:
    def __init__(self):
        self.missions = []

    def add_mission(self, mission: Mission):
        self.missions.append(mission)

    def check(self, model):
        completed = []
        for m in self.missions:
            if not m.completed and m.condition(model):
                m.completed = True
                completed.append(m)
        return completed
