class ShopController:
    def __init__(self, model, message_callback, refresh_callback):
        self.model = model
        self.set_message = message_callback
        self.refresh_all = refresh_callback

    def shop_buy_fert(self, fert_id):
        ok, msg = self.model.buy_fertilizer(fert_id)
        self.set_message(msg)
        self.refresh_all()

    def shop_sell_crop(self, plant_name):
        ok, msg = self.model.sell_from_barn(plant_name)
        self.set_message(msg)
        self.refresh_all()
