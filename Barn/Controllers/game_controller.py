from Services.resource_service import ResourceService
from Models.model import GameModel
from View.view import GameView, ShopWindow, BarnWindow
from Controllers.plot_controller import PlotController
from Controllers.shop_controller import ShopController
from Controllers.barn_controller import BarnController
from Controllers.timer_controller import TimerController
from Controllers.mission_controller import MissionController
from Services.logger_service import LoggerService
from Missions.mission import Mission


class GameController:
    def __init__(self, root):
        self.model = GameModel()
        self.view = GameView(root, max_plots=GameModel.MAX_PLOTS)
        self.logger = LoggerService.get_logger()
        self.logger.info("[SYSTEM] GameController initialized")

        self.shop_window = None
        self.barn_window = None

        ResourceService.load_game(self.model)
        mm = self.model.mission_model

        mm.add_mission(Mission(1, "First Sprout", "Plant your first crop",
                               lambda m: m.stats["plants_planted"] >= 1, 20))
        mm.add_mission(Mission(2, "Gardener", "Plant 10 crops",
                               lambda m: m.stats["plants_planted"] >= 10, 50))
        mm.add_mission(Mission(3, "Farmer", "Plant 50 crops",
                               lambda m: m.stats["plants_planted"] >= 50, 150))
        mm.add_mission(Mission(4, "Agrarian Tycoon", "Plant 200 crops",
                               lambda m: m.stats["plants_planted"] >= 200, 500))

        mm.add_mission(Mission(5, "First Harvest", "Harvest your first crop",
                               lambda m: m.stats["plants_harvested"] >= 1, 20))
        mm.add_mission(Mission(6, "Harvest Time", "Harvest 25 crops",
                               lambda m: m.stats["plants_harvested"] >= 25, 100))
        mm.add_mission(Mission(7, "Combine Machine", "Harvest 100 crops",
                               lambda m: m.stats["plants_harvested"] >= 100, 300))

        mm.add_mission(Mission(8, "Junior Chemist", "Use 5 fertilizers",
                               lambda m: m.stats["fertilizers_used"] >= 5, 50))
        mm.add_mission(Mission(9, "Chemist", "Use 25 fertilizers",
                               lambda m: m.stats["fertilizers_used"] >= 25, 150))
        mm.add_mission(Mission(10, "Pro Chemist", "Use 100 fertilizers",
                               lambda m: m.stats["fertilizers_used"] >= 100, 500))

        mm.add_mission(Mission(11, "Small Farm", "Buy your first extra plot",
                               lambda m: m.stats["plots_bought"] >= 1, 100))
        mm.add_mission(Mission(12, "Land Expansion", "Buy 5 new plots",
                               lambda m: m.stats["plots_bought"] >= 5, 300))
        mm.add_mission(Mission(13, "Farm Empire", "Buy all available plots",
                               lambda m: len(m.plots) >= m.MAX_PLOTS, 1000))

        mm.add_mission(Mission(14, "First Sale", "Sell any crop",
                               lambda m: m.stats["sold_income"] > 0, 50))
        mm.add_mission(Mission(15, "Small Trader", "Earn 50 coins from sales",
                               lambda m: m.stats["sold_income"] >= 50, 100))
        mm.add_mission(Mission(16, "Merchant", "Earn 200 coins from sales",
                               lambda m: m.stats["sold_income"] >= 200, 300))

        mm.add_mission(Mission(17, "Golden Hands", "Reach a balance of 500 coins",
                               lambda m: m.balance >= 500, 200))
        mm.add_mission(Mission(18, "Farmer Forever", "Plant 1000 crops",
                               lambda m: m.stats["plants_planted"] >= 1000, 2000))
        mm.add_mission(Mission(19, "Empire", "Harvest 1000 crops",
                               lambda m: m.stats["plants_harvested"] >= 1000, 3000))
        self.mission_controller = MissionController(
            self.model,
            mm,
            self.set_message,
            self.refresh_all
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
                self.view.update_plot(i, "Empty", ResourceService.get_item("empty"),
                                      "Plant", "normal")
            elif plot.state == "growing":
                plant = plot.plant
                remaining = max(0, plot.remaining_time)
                stage = self.model.get_plot_stage_index(plot)
                self.view.update_plot(
                    i,
                    f"Growing {plant.name} ({remaining}s)",
                    ResourceService.get_item(f"{plant.image_prefix}_{stage}"),
                    "Growing...",
                    "disabled"
                )
            elif plot.state == "ready":
                plant = plot.plant
                self.view.update_plot(
                    i,
                    f"Ready: {plant.name}",
                    ResourceService.get_item(f"{plant.image_prefix}_{plant.stages}"),
                    "Harvest",
                    "normal"
                )

        for j in range(len(self.model.plots), self.view.max_plots):
            self.view.update_plot(j, "Locked",
                                  ResourceService.get_item("empty"),
                                  "Locked", "disabled")

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

    def get_plot_stage_index(self, plot):
        if plot is None or plot.state == "empty" or plot.plant is None:
            return 0
        plant = plot.plant

        if plot.state == "ready":
            return plant.stages

        total = getattr(plot, "total_time", 0)
        remaining = getattr(plot, "remaining_time", 0)

        if total <= 0:
            return 1
        elapsed = max(0, total - remaining)
        part = total / plant.stages
        stage = int(elapsed / part) + 1
        if stage < 1:
            stage = 1
        if stage > plant.stages:
            stage = plant.stages

        return stage
