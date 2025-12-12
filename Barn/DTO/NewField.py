class NewFieldDTO:
    def __init__(self, with_fertilizer: bool = False, fert_boost: int = 0):
        self.with_fertilizer = with_fertilizer
        self.fert_boost = fert_boost
