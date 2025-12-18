from Services.logger_service import LoggerService

class MissionController:
    def __init__(self, model, mission_model, set_message, refresh_all):
        self.model = model
        self.mission_model = mission_model
        self.set_message = set_message
        self.refresh_all = refresh_all
        self.logger = LoggerService.get_logger()

        self.logger.info("[SYSTEM] MissionController initialized")

    def check_missions(self):
        completed = self.mission_model.check(self.model)

        for mission in completed:
            self.model.balance += mission.reward

            self.logger.info(
                f"[ACHIEVEMENT] Mission completed: "
                f"{mission.title} (+${mission.reward})"
            )

            self.set_message(
                f"Mission completed: {mission.title} (+${mission.reward})"
            )

        if completed:
            self.refresh_all()
