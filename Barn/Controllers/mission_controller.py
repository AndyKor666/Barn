from Services.Logger_service import LoggerService

class MissionController:
    def __init__(self, model, mission_model, set_message, refresh_all):
        self.model = model
        self.mission_model = mission_model
        self.set_message = set_message
        self.refresh_all = refresh_all
        self.logger = LoggerService.get_logger()

    def check_missions(self):
        completed = self.mission_model.check(self.model)
        for m in completed:
            self.model.balance += m.reward
            self.set_message(f"Mission completed: {m.title} (+{m.reward})")
            self.logger.info(f"[MISSION] Completed: {m.title}")
        if completed:
            self.refresh_all()
