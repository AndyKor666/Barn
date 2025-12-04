class Plant:
    def __init__(self, id, name, base_grow_time, sell_price, stages, asset_prefix):
        self.id = id
        self.name = name
        self.base_grow_time = base_grow_time
        self.sell_price = sell_price
        self.stages = stages
        self.asset_prefix = asset_prefix
