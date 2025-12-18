from Services.logger_service import LoggerService


class BarnController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.logger = LoggerService.get_logger()

        self.logger.info("[SYSTEM] BarnController initialized")