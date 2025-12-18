from Services.logger_service import LoggerService

class PlotController:
    def __init__(self, model, view, set_message, refresh_all, mission_controller):
        self.model = model
        self.view = view
        self.set_message = set_message
        self.refresh_all = refresh_all
        self.mission_controller = mission_controller
        self.logger = LoggerService.get_logger()

    def on_plot_button(self, index):
        plot = self.model.plots[index]

        if plot.state == "empty":
            plant_name = self.view.plant_combo.get()
            plant = next(p for p in self.model.plants if p.name == plant_name)
            fert_name = self.view.fert_combo.get()
            fert = next((f for f in self.model.fertilizers if f.name == fert_name), None)

            ok, msg = self.model.plant_crop(
                index,
                plant.id,
                fert.id if fert_name != "None" else None
            )
            self.set_message(msg)

        elif plot.state == "ready":
            ok, msg = self.model.harvest(index)
            self.set_message(msg)

        self.mission_controller.check_missions()
        self.refresh_all()
