from Services.resource_service import ResourceService

class TimerController:
    def __init__(self, model, view, refresh_plots, set_message):
        self.model = model
        self.view = view
        self.refresh_plots = refresh_plots
        self.set_message = set_message
    def autosave(self):
        ResourceService.save_game(self.model)
        self.view.root.after(30000, self.autosave)
    def schedule_tick(self):
        just_ready = self.model.tick()
        if just_ready:
            names = ", ".join({p.plant.name for p in just_ready if p.plant})
            self.set_message(f"Ready to harvest: {names}")
        self.refresh_plots()
        self.view.root.after(1000, self.schedule_tick)
