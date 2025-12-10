from Models.plant import Plant

class Carrot(Plant):
    def __init__(self):
        super().__init__(
            pid=2,
            name="Carrot",
            base_grow_time=10,
            sell_price=15,
            stages=4,
            image_prefix="carrot"
        )
