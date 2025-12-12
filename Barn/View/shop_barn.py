from DTO.NewField import NewFieldDTO

class ShopController:
    def __init__(self, model, set_message, refresh_all):
        self.model = model
        self.set_message = set_message
        self.refresh_all = refresh_all

    def shop_buy_fert(self, fert_id):
        ok, msg = self.model.buy_fertilizer(fert_id)
        self.set_message(msg)
        if ok:
            self.refresh_all()

    def shop_sell_crop(self, plant_name, count):
        for _ in range(count):
            ok, msg = self.model.sell_from_barn(plant_name)
            if not ok:
                return False, msg
        return True, msg

    def buy_new_plot(self, with_fertilizer: bool):
        dto = NewFieldDTO(
            with_fertilizer=with_fertilizer,
            fert_boost=5 if with_fertilizer else 0
        )
        ok, msg = self.model.buy_new_plot(dto)
        self.set_message(msg)
        if ok:
            self.refresh_all()
        return ok, msg
