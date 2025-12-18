from DTO.NewField import NewFieldDTO
from Services.logger_service import LoggerService

class ShopController:
    def __init__(self, model, set_message, refresh_all, mission_controller):
        self.model = model
        self.set_message = set_message
        self.refresh_all = refresh_all
        self.mission_controller = mission_controller
        self.logger = LoggerService.get_logger()

    def shop_buy_fert(self, fid):
        ok, msg = self.model.buy_fertilizer(fid)
        self.set_message(msg)
        if ok:
            self.mission_controller.check_missions()
            self.refresh_all()

    def shop_sell_crop(self, name, count):
        for _ in range(count):
            self.model.sell_from_barn(name)
        self.mission_controller.check_missions()
        self.refresh_all()
        return True, "Sold"

    def buy_new_plot(self, with_fertilizer):
        dto = NewFieldDTO(with_fertilizer, 5 if with_fertilizer else 0)
        ok, msg = self.model.buy_new_plot(dto)
        self.set_message(msg)
        if ok:
            self.mission_controller.check_missions()
            self.refresh_all()
        return ok, msg
