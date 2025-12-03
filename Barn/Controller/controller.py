from Model.model import GameModel
from View.view import GameView, ShopWindow, BarnWindow

class GameController:
    def __init__(self, root):
        self.model = GameModel()
        self.view = GameView(root)
        self.shop_window = None
        self.barn_window = None

        for i, btn in enumerate(self.view.plot_buttons):
            btn.config(command=lambda idx=i: self.on_plot_button(idx))
        self.view.open_shop_button.config(command=self.open_shop)
        self.view.open_barn_button.config(command=self.open_barn)
        self.view.set_plant_options([p.name for p in self.model.plants])
        self.view.set_fert_options([f.name for f in self.model.fertilizers])
        self.refresh_all()
        self.schedule_tick()

    def schedule_tick(self):
        just_ready = self.model.tick()
        if just_ready:
            names = ", ".join(f"{pl.plant.name} on plot {pl.id}" for pl in just_ready)
            self.set_message(f"Ready to harvest: {names}")
        self.refresh_plots()
        self.view.root.after(1000, self.schedule_tick)

    def refresh_all(self):
        self.view.set_balance(self.model.balance)
        self.refresh_plots()
        self.refresh_fertilizer_inventory()
        self.refresh_barn_summary()
        if self.shop_window is not None and self.shop_window.winfo_exists():
            self.shop_window.refresh()

    def refresh_plots(self):
        for i, plot in enumerate(self.model.plots):
            img_name = None
            if plot.state == "empty":
                text = "Empty"
                self.view.plot_buttons[i].config(text="Plant", state="normal")
                img_name = "empty.png"
            elif plot.state == "growing":
                text = f"Growing {plot.plant.name} ({plot.remaining_time}s)"
                self.view.plot_buttons[i].config(text="Growing...", state="disabled")
                stage = self.model.get_plot_stage_index(plot)
                img_name = f"{plot.plant.image_prefix}_{stage}.png"
            elif plot.state == "ready":
                text = f"Ready: {plot.plant.name}"
                self.view.plot_buttons[i].config(text="Harvest", state="normal")
                stage = plot.plant.stage_count
                img_name = f"{plot.plant.image_prefix}_{stage}.png"
            else:
                text = "Unknown"
                img_name = "empty.png"
            self.view.update_plot(i, text, img_name)

    def refresh_fertilizer_inventory(self):
        lines = []
        for f in self.model.fertilizers:
            count = self.model.fertilizer_inventory.get(f.id, 0)
            lines.append(f"{f.name}: {count}")
        self.view.update_fertilizer_inventory("\n".join(lines))

    def refresh_barn_summary(self):
        if not self.model.barn:
            text = "(empty)"
        else:
            parts = [f"{k} x{v}" for k, v in sorted(self.model.barn.items())]
            text = ", ".join(parts)
        self.view.set_barn_summary(text)

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
            self.set_message("Select a plant first")
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

    def set_message(self, msg):
        self.view.set_message(msg)

    def open_shop(self):
        if self.shop_window is not None and self.shop_window.winfo_exists():
            self.shop_window.lift()
            return
        self.shop_window = ShopWindow(self.view.root, self.model, self)

    def open_barn(self):
        if self.barn_window is not None and self.barn_window.winfo_exists():
            self.barn_window.lift()
            return
        self.barn_window = BarnWindow(self.view.root, self.model, self)

    def shop_buy_fert(self, fert_id):
        ok, msg = self.model.buy_fertilizer(fert_id)
        self.set_message(msg)
        self.refresh_all()

    def shop_sell_crop(self, plant_name):
        ok, msg = self.model.sell_from_barn(plant_name)
        self.set_message(msg)
        self.refresh_all()
