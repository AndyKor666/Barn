class PlotController:
    def __init__(self, model, view, set_message, refresh_all):
        self.model = model
        self.view = view
        self.set_message = set_message
        self.refresh_all = refresh_all

    def on_plot_button(self, index):
        if index >= len(self.model.plots):
            self.set_message("This plot is locked. Buy a new plot in the shop.")
            return

        plot = self.model.plots[index]

        if plot.state == "empty":
            plant_name = self.view.plant_combo.get()
            if not plant_name:
                self.set_message("Select a plant first.")
                return

            plant = next((p for p in self.model.plants if p.name == plant_name), None)
            if plant is None:
                self.set_message("Unknown plant.")
                return

            fert_name = self.view.fert_combo.get()
            fert_id = None
            if fert_name and fert_name != "None":
                fert = next(
                    (f for f in self.model.fertilizers if f.name == fert_name),
                    None
                )
                if fert is None:
                    self.set_message("Unknown fertilizer.")
                    return
                fert_id = fert.id

            ok, msg = self.model.plant_crop(index, plant.id, fert_id)
            self.set_message(msg)
            if ok:
                self.refresh_all()

        elif plot.state == "ready":
            ok, msg = self.model.harvest(index)
            self.set_message(msg)
            if ok:
                self.refresh_all()

        elif plot.state == "growing":
            self.set_message("This crop is still growing...")
