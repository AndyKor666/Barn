class BarnController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def refresh_barn_summary(self):
        if not self.model.barn:
            txt = "(empty)"
        else:
            txt = ", ".join(f"{k} x{v}" for k, v in sorted(self.model.barn.items()))
        self.view.set_barn_summary(txt)
