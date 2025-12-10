class TimerController:
    def __init__(self, model, view, refresh_plots, set_message):
        self.model = model
        self.view = view
        self.refresh_plots = refresh_plots
        self.set_message = set_message

    def autosave(self):
        self.model.save_game()
        self.view.root.after(3000, self.autosave)

    def schedule_tick(self):
        just_ready = self.model.tick()

        if just_ready:
            names = ", ".join(f"{pl.plant.name} on plot {pl.id}" for pl in just_ready)
            self.set_message(f"Ready to harvest: {names}")

        self.refresh_plots()
        self.view.root.after(1000, self.schedule_tick)
