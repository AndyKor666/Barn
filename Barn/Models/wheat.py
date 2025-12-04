from Models.plant import Plant

class Wheat(Plant):
    def __init__(self):
        super().__init__(
            id=3,
            name="Wheat",
            base_grow_time=8,
            sell_price=12,
            stages=4,
            asset_prefix="wheat"
        )
