from Services.Resource_service import ResourceService
from Models.model import GameModel
from View.view import GameView, ShopWindow, BarnWindow
from Controllers.plot_controller import PlotController
from Controllers.shop_controller import ShopController
from Controllers.barn_controller import BarnController
from Controllers.timer_controller import TimerController
from Controllers.mission_controller import MissionController
from Services.logger_service import LoggerService
from Models.mission_model import Mission


class GameController:
    def __init__(self, root):
        self.model = GameModel()
        self.view = GameView(root, max_plots=GameModel.MAX_PLOTS)
        self.logger = LoggerService.get_logger()
        self.logger.info("[SYSTEM] GameController initialized")
        self.shop_window = None
        self.barn_window = None
        ResourceService.load_game(self.model)

        self.mission_controller = MissionController(
            self.model,
            self.model.mission_model,
            self.set_message,
            self.refresh_all,
        )
        self.plot_controller = PlotController(
            self.model,
            self.view,
            self.set_message,
            self.refresh_all,
            self.mission_controller
        )
        self.shop_controller = ShopController(
            self.model,
            self.set_message,
            self.refresh_all,
            self.mission_controller
        )
        self.barn_controller = BarnController(self.model, self.view)

        self.timer_controller = TimerController(
            self.model,
            self.view,
            self.refresh_plots,
            self.set_message
        )
        for i, btn in enumerate(self.view.plot_buttons):
            btn.config(command=lambda idx=i: self.plot_controller.on_plot_button(idx))

        self.view.open_shop_button.config(command=self.open_shop)
        self.view.open_barn_button.config(command=self.open_barn)

        self.view.set_plant_options([p.name for p in self.model.plants])
        self.view.set_fert_options([f.name for f in self.model.fertilizers])

        self.model.mission_model.add_mission(
            Mission(
                mid=1,
                title="First harvest",
                description="Harvest any crop once",
                reward=50,
                condition=lambda m: sum(m.barn.values()) >= 1
            )
        )
        self.model.mission_model.add_mission(
            Mission(
                mid=2,
                title="Farmer",
                description="Harvest 5 crops",
                reward=150,
                condition=lambda m: sum(m.barn.values()) >= 5
            )
        )
        self.model.mission_model.add_mission(
            Mission(
                mid=3,
                title="Businessman",
                description="Earn $200",
                reward=200,
                condition=lambda m: m.balance >= 200
            )
        )
        self.refresh_all()
        self.timer_controller.autosave()
        self.timer_controller.schedule_tick()

    def refresh_all(self):
        self.view.set_balance(self.model.balance)
        self.refresh_plots()
        self.refresh_fertilizer_inventory()

        if self.shop_window and self.shop_window.winfo_exists():
            self.shop_window.refresh()

        if self.barn_window and self.barn_window.winfo_exists():
            self.barn_window.refresh()

    def refresh_plots(self):
        for i, plot in enumerate(self.model.plots):
            if plot.state == "empty":
                self.view.update_plot(
                    i, "Empty",
                    ResourceService.get_item("empty"),
                    button_text="Plant",
                    button_state="normal"
                )
            elif plot.state == "growing":
                plant = plot.plant
                remaining = max(0, plot.remaining_time)
                total = plant.base_grow_time
                stages = plant.stages
                elapsed = max(0, total - remaining)
                stage = max(1, min(stages, int(elapsed / (total / stages)) + 1))

                self.view.update_plot(
                    i,
                    f"Growing {plant.name} ({remaining}s)",
                    ResourceService.get_item(f"{plant.image_prefix}_{stage}"),
                    button_text="Growing...",
                    button_state="disabled"
                )
            elif plot.state == "ready":
                plant = plot.plant
                self.view.update_plot(
                    i,
                    f"Ready: {plant.name}",
                    ResourceService.get_item(f"{plant.image_prefix}_{plant.stages}"),
                    button_text="Harvest",
                    button_state="normal"
                )

        for j in range(len(self.model.plots), self.view.max_plots):
            self.view.update_plot(
                j,
                "Locked",
                ResourceService.get_item("empty"),
                button_text="Locked",
                button_state="disabled"
            )

    def refresh_fertilizer_inventory(self):
        lines = [
            f"{f.name}: {self.model.fertilizer_inventory.get(f.id, 0)}"
            for f in self.model.fertilizers
        ]
        self.view.update_fertilizer_inventory("\n".join(lines))

    def open_shop(self):
        if self.shop_window and self.shop_window.winfo_exists():
            self.shop_window.lift()
            return
        self.logger.info("[UI] Shop opened")
        self.shop_window = ShopWindow(self.view.root, self.model, self)

    def open_barn(self):
        if self.barn_window and self.barn_window.winfo_exists():
            self.barn_window.lift()
            return
        self.logger.info("[UI] Barn opened")
        self.barn_window = BarnWindow(self.view.root, self.model, self)

    def set_message(self, msg):
        self.view.set_message(msg)

    def shop_buy_fert(self, fert_id):
        self.shop_controller.shop_buy_fert(fert_id)

    def shop_sell_crop(self, plant_name, count):
        return self.shop_controller.shop_sell_crop(plant_name, count)

    def shop_buy_new_plot(self, with_fertilizer: bool):
        return self.shop_controller.buy_new_plot(with_fertilizer)
