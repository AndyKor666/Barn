from Services.Resource_service import ResourceService
from Models.model import GameModel
from View.view import GameView, ShopWindow, BarnWindow
from Controllers.plot_controller import PlotController
from Controllers.shop_controller import ShopController
from Controllers.barn_controller import BarnController
from Controllers.timer_controller import TimerController


class GameController:
    def __init__(self, root):
        self.model = GameModel()
        self.view = GameView(root, max_plots=GameModel.MAX_PLOTS)

        self.shop_window = None
        self.barn_window = None

   
        ResourceService.load_game(self.model)

        self.plot_controller = PlotController(
            self.model, self.view, self.set_message, self.refresh_all
        )

        self.shop_controller = ShopController(
            self.model, self.set_message, self.refresh_all
        )

        self.barn_controller = BarnController(self.model, self.view)

        self.timer_controller = TimerController(
            self.model, self.view, self.refresh_plots, self.set_message
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
        self.barn_controller.refresh_barn_summary()

        if self.shop_window and self.shop_window.winfo_exists():
            self.shop_window.refresh()

        if self.barn_window and self.barn_window.winfo_exists():
            self.barn_window.refresh()

    def refresh_plots(self):
        from Services.Resource_service import ResourceService
        for i, plot in enumerate(self.model.plots):
            if plot.state == "empty":
                text = "Empty"
                img_path = ResourceService.get_item("empty")
                self.view.update_plot(
                    i, text, img_path,
                    button_text="Plant", button_state="normal"
                )

            elif plot.state == "growing":
                plant = plot.plant
                remaining = max(0, plot.remaining_time)

                text = f"Growing {plant.name} ({remaining}s)"

                total = plant.base_grow_time
                stages = plant.stages
                elapsed = total - remaining
                if elapsed < 0:
                    elapsed = 0

                stage = max(1, min(stages, int(elapsed / (total / stages)) + 1))
                key = f"{plant.image_prefix}_{stage}"
                img_path = ResourceService.get_item(key)

                self.view.update_plot(
                    i, text, img_path,
                    button_text="Growing...", button_state="disabled"
                )

            elif plot.state == "ready":
                plant = plot.plant
                text = f"Ready: {plant.name}"
                key = f"{plant.image_prefix}_{plant.stages}"
                img_path = ResourceService.get_item(key)

                self.view.update_plot(
                    i, text, img_path,
                    button_text="Harvest", button_state="normal"
                )
        for j in range(len(self.model.plots), self.view.max_plots):
            from Services.Resource_service import ResourceService
            img_path = ResourceService.get_item("empty")
            self.view.update_plot(
                j, "Locked", img_path,
                button_text="Locked", button_state="disabled"
            )

    def refresh_fertilizer_inventory(self):
        lines = []
        for f in self.model.fertilizers:
            count = self.model.fertilizer_inventory.get(f.id, 0)
            lines.append(f"{f.name}: {count}")
        self.view.update_fertilizer_inventory("\n".join(lines))

    def open_shop(self):
        if self.shop_window and self.shop_window.winfo_exists():
            self.shop_window.lift()
            return
        self.shop_window = ShopWindow(self.view.root, self.model, self)

    def open_barn(self):
        if self.barn_window and self.barn_window.winfo_exists():
            self.barn_window.lift()
            return
        self.barn_window = BarnWindow(self.view.root, self.model, self)

    def set_message(self, msg):
        self.view.set_message(msg)

    def shop_buy_fert(self, fert_id):
        self.shop_controller.shop_buy_fert(fert_id)

    def shop_sell_crop(self, plant_name, count):
        return self.shop_controller.shop_sell_crop(plant_name, count)

    def shop_buy_new_plot(self, with_fertilizer: bool):
        self.shop_controller.buy_new_plot(with_fertilizer)
