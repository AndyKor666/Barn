class Mission:
    def __init__(self, mid, title, description, condition, reward):
        self.id = mid
        self.title = title
        self.description = description
        self.condition = condition
        self.reward = reward
        self.completed = False
