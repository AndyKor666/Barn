class Plant:
    def __init__(self, pid, name, base_grow_time, sell_price, stages, image_prefix):
        self.id = pid
        self.name = name
        self.base_grow_time = base_grow_time
        self.sell_price = sell_price
        self.stages = stages
        self.image_prefix = image_prefix
