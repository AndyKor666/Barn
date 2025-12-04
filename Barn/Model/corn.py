from Model.plant import Plant

class Corn(Plant):
    def __init__(self):
        super().__init__(
            id=1,
            name="Corn",
            base_grow_time=12,
            sell_price=20,
            stages=4,
            asset_prefix="corn"
        )
