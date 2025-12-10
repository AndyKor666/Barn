class PlotController:
    def __init__(self, model, view, message_callback, refresh_callback):
        self.model = model
        self.view = view
        self.set_message = message_callback
        self.refresh_all = refresh_callback

    def on_plot_button(self, index):
        plot = self.model.plots[index]
        if plot.state == "empty":
            self.handle_plant(index)
        elif plot.state == "ready":
            self.handle_harvest(index)

    def handle_plant(self, index):
        plant_name = self.view.plant_combo.get()
        plant = next((p for p in self.model.plants if p.name == plant_name), None)

        if plant is None:
            self.set_message("Select a plant")
            return

        fert_name = self.view.fert_combo.get()
        fert_id = None

        if fert_name != "(none)":
            fert = next((f for f in self.model.fertilizers if f.name == fert_name), None)
            if fert:
                fert_id = fert.id

        ok, msg = self.model.plant_crop(index, plant.id, fert_id)
        self.set_message(msg)
        self.refresh_all()

    def handle_harvest(self, index):
        ok, msg = self.model.harvest(index)
        self.set_message(msg)
        self.refresh_all()
