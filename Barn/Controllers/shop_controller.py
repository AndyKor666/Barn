from DTO.NewField import NewFieldDTO
from Services.logger_service import LoggerService

class ShopController:
    def __init__(self, model, set_message, refresh_all):
        self.model = model
        self.set_message = set_message
        self.refresh_all = refresh_all
        self.logger = LoggerService.get_logger()

        self.logger.info("[SYSTEM] ShopController initialized")

    def shop_buy_fert(self, fert_id):
        ok, msg = self.model.buy_fertilizer(fert_id)
        self.set_message(msg)

        if ok:
            fert = self.model.get_fertilizer_by_id(fert_id)
            self.logger.info(f"[SHOP] Bought fertilizer: {fert.name}")
            self.refresh_all()
        else:
            self.logger.info(f"[SHOP] Failed to buy fertilizer (id={fert_id})")

    def shop_sell_crop(self, plant_name, count):
        if count <= 0:
            self.logger.info(f"[SHOP] Invalid sell count: {count}")
            return False, "Invalid count"

        sold = 0

        for _ in range(count):
            ok, msg = self.model.sell_from_barn(plant_name)
            if not ok:
                self.logger.info(
                    f"[SHOP] Sell failed: {plant_name}, sold={sold}"
                )
                return False, msg
            sold += 1

        self.logger.info(
            f"[SHOP] Sold {sold}x {plant_name}"
        )
        return True, f"Sold {sold}x {plant_name}"

    def buy_new_plot(self, with_fertilizer: bool):
        dto = NewFieldDTO(
            with_fertilizer=with_fertilizer,
            fert_boost=5 if with_fertilizer else 0
        )

        ok, msg = self.model.buy_new_plot(dto)
        self.set_message(msg)

        if ok:
            self.logger.info(
                f"[SHOP] New plot purchased "
                f"(with_fertilizer={with_fertilizer})"
            )
            self.refresh_all()
        else:
            self.logger.info(
                f"[SHOP] Failed to buy new plot "
                f"(with_fertilizer={with_fertilizer})"
            )
        return ok, msg
