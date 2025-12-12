from Models.plant import Plant

class Wheat(Plant):
    def __init__(self):
        super().__init__(
            pid=3,
            name="Wheat",
            base_grow_time=14,
            sell_price=25,
            stages=4,
            image_prefix="wheat",
        )
