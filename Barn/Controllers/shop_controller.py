from Services.logger_service import LoggerService
from DTO.NewField import NewFieldDTO


class ShopController:
    def __init__(self, model, set_message, refresh_all, mission_controller):
        self.model = model
        self.set_message = set_message
        self.refresh_all = refresh_all
        self.mission_controller = mission_controller
        self.logger = LoggerService.get_logger()

        self.logger.info("[SYSTEM] ShopController initialized")

    def shop_buy_fert(self, fert_id):
        ok, msg = self.model.buy_fertilizer(fert_id)
        self.set_message(msg)

        if ok:
            self.logger.info(f"[SHOP] Fertilizer bought (id={fert_id})")
            self.refresh_all()
            self.mission_controller.check_missions()

    def shop_sell_crop(self, plant_name, count):
        if count <= 0:
            return False, "Invalid count"

        last_msg = None
        for _ in range(count):
            ok, msg = self.model.sell_from_barn(plant_name)
            if not ok:
                return False, msg
            last_msg = msg

        self.logger.info(f"[SHOP] Sold {count}x {plant_name}")
        self.refresh_all()
        self.mission_controller.check_missions()
        return True, last_msg

    def buy_new_plot(self, with_fertilizer: bool):
        dto = NewFieldDTO(
            with_fertilizer=with_fertilizer,
            fert_boost=5 if with_fertilizer else 0
        )

        ok, msg = self.model.buy_new_plot(dto)
        self.set_message(msg)

        if ok:
            self.logger.info(
                f"[SHOP] New plot bought (fertilizer={with_fertilizer})"
            )
            self.refresh_all()
            self.mission_controller.check_missions()

        return ok, msg
