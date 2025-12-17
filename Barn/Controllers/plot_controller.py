from Services.logger_service import LoggerService

class PlotController:
    def __init__(self, model, view, set_message, refresh_all):
        self.model = model
        self.view = view
        self.set_message = set_message
        self.refresh_all = refresh_all
        self.logger = LoggerService.get_logger()

        self.logger.info("[SYSTEM] PlotController initialized")

    def on_plot_button(self, index):
        if index >= len(self.model.plots):
            self.set_message("This plot is locked. Buy a new plot in the shop.")
            self.logger.info(f"[PLOT] Attempt to use locked plot {index + 1}")
            return

        plot = self.model.plots[index]
        if plot.state == "empty":
            plant_name = self.view.plant_combo.get()
            if not plant_name:
                self.set_message("Select a plant first.")
                self.logger.info("[PLOT] Planting failed: no plant selected")
                return

            plant = next((p for p in self.model.plants if p.name == plant_name), None)
            if plant is None:
                self.set_message("Unknown plant.")
                self.logger.info(f"[PLOT] Unknown plant selected: {plant_name}")
                return

            fert_name = self.view.fert_combo.get()
            fert_id = None

            if fert_name and fert_name != "None":
                fert = next((f for f in self.model.fertilizers if f.name == fert_name), None)
                if fert is None:
                    self.set_message("Unknown fertilizer.")
                    self.logger.info(f"[PLOT] Unknown fertilizer: {fert_name}")
                    return
                fert_id = fert.id

            ok, msg = self.model.plant_crop(index, plant.id, fert_id)
            self.set_message(msg)

            if ok:
                self.logger.info(
                    f"[PLOT] Planted {plant.name} on plot {index + 1} "
                    f"(fertilizer={fert_name})"
                )
                self.refresh_all()
        elif plot.state == "ready":
            plant_name = plot.plant.name if plot.plant else "Unknown"

            ok, msg = self.model.harvest(index)
            self.set_message(msg)

            if ok:
                self.logger.info(
                    f"[HARVEST] {plant_name} harvested from plot {index + 1}"
                )
                self.refresh_all()

        elif plot.state == "growing":
            self.set_message("This crop is still growing...")
            self.logger.info(
                f"[INFO] Plot {index + 1} clicked but crop is still growing"
            )
