from Models.plant import Plant

class Carrot(Plant):
    def __init__(self):
        super().__init__(
            id=2,
            name="Carrot",
            base_grow_time=6,
            sell_price=8,
            stages=4,
            asset_prefix="carrot"
        )
