from Services.logger_service import LoggerService


class PlotController:
    def __init__(self, model, view, set_message, refresh_all, mission_controller):
        self.model = model
        self.view = view
        self.set_message = set_message
        self.refresh_all = refresh_all
        self.mission_controller = mission_controller
        self.logger = LoggerService.get_logger()

        self.logger.info("[SYSTEM] PlotController initialized")

    def on_plot_button(self, index):
        if index >= len(self.model.plots):
            self.set_message("This plot is locked.")
            self.logger.info(f"[PLOT] Locked plot clicked: {index + 1}")
            return

        plot = self.model.plots[index]

        if plot.state == "empty":
            plant_name = self.view.plant_combo.get()
            if not plant_name:
                self.set_message("Select a plant first.")
                return

            plant = next((p for p in self.model.plants if p.name == plant_name), None)
            if not plant:
                self.set_message("Unknown plant.")
                return

            fert_name = self.view.fert_combo.get()
            fert_id = None

            if fert_name and fert_name != "None":
                fert = next(
                    (f for f in self.model.fertilizers if f.name == fert_name),
                    None
                )
                if not fert:
                    self.set_message("Unknown fertilizer.")
                    return
                fert_id = fert.id

            ok, msg = self.model.plant_crop(index, plant.id, fert_id)
            self.set_message(msg)

            if ok:
                self.logger.info(
                    f"[PLOT] Planted {plant.name} on plot {index + 1}"
                )
                self.refresh_all()
                self.mission_controller.check_missions()

        elif plot.state == "ready":
            plant_name = plot.plant.name if plot.plant else "Unknown"

            ok, msg = self.model.harvest(index)
            self.set_message(msg)

            if ok:
                self.logger.info(
                    f"[HARVEST] {plant_name} harvested from plot {index + 1}"
                )
                self.refresh_all()
                self.mission_controller.check_missions()

        elif plot.state == "growing":
            self.set_message("This crop is still growing...")
