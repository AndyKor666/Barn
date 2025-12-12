from Models.plant import Plant

class Corn(Plant):
    def __init__(self):
        super().__init__(
            pid=1,
            name="Corn",
            base_grow_time=12,
            sell_price=20,
            stages=4,
            image_prefix="corn",
        )
