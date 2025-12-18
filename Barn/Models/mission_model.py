class Mission:
    def __init__(self, mid, title, description, reward, condition):
        self.id = mid
        self.title = title
        self.description = description
        self.reward = reward
        self.condition = condition
        self.completed = False

class MissionModel:
    def __init__(self):
        self.missions = []

    def add_mission(self, mission):
        self.missions.append(mission)

    def check(self, model):
        completed_now = []

        for mission in self.missions:
            if not mission.completed and mission.condition(model):
                mission.completed = True
                completed_now.append(mission)

        return completed_now
