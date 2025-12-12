class BarnController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def refresh_barn_summary(self):
        if not self.model.barn:
            self.view.set_barn_summary("(empty)")
            return

        parts = [f"{name} x{count}" for name, count in sorted(self.model.barn.items())]
        self.view.set_barn_summary(", ".join(parts))
