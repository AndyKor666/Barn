import os
import json
from Models.wheat import Wheat
from Models.carrot import Carrot
from Models.corn import Corn

SAVE_FILE = "save.json"

class Plant:
    def __init__(self, pid, name, base_grow_time, sell_price, stage_count, image_prefix):
        self.id = pid
        self.name = name
        self.base_grow_time = base_grow_time
        self.sell_price = sell_price
        self.stage_count = stage_count
        self.image_prefix = image_prefix

class Fertilizer:
    def __init__(self, fid, name, price, multiplier):
        self.id = fid
        self.name = name
        self.price = price
        self.multiplier = multiplier

class FarmPlot:
    def __init__(self, pid):
        self.id = pid
        self.state = "empty"
        self.plant = None
        self.remaining_time = 0
        self.total_time = 0

class GameModel:
    def __init__(self):
        self.balance = 50
        self.plants = [Corn(), Carrot(), Wheat()]
        self.fertilizers = [
            Fertilizer(1, "Basic Fertilizer", 10, 0.80),
            Fertilizer(2, "Super Fertilizer", 20, 0.50),
        ]

        self.fertilizer_inventory = {f.id: 0 for f in self.fertilizers}

        self.barn = {}
        self.plots = [FarmPlot(i) for i in range(1, 4)]

#----------------------------------------------------------------------------

    def save_game(self):
        data = {
            "balance": self.balance,
            "barn": self.barn,
            "fertilizers": self.fertilizer_inventory,
            "plots": []
        }

        for plot in self.plots:
            if plot.state == "empty":
                data["plots"].append({
                    "state": "empty"
                })
            elif plot.state == "growing":
                data["plots"].append({
                    "state": "growing",
                    "plant_id": plot.plant.id,
                    "remaining_time": plot.remaining_time,
                    "total_time": plot.total_time
                })
            elif plot.state == "ready":
                data["plots"].append({
                    "state": "ready",
                    "plant_id": plot.plant.id
                })

        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            return
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            return
        self.balance = data.get("balance", 50)
        self.barn = data.get("barn", {})

        self.fertilizer_inventory = data.get("fertilizers", {})
        self.fertilizer_inventory = {
            int(k): v for k, v in self.fertilizer_inventory.items()
        }
        plots_data = data.get("plots", [])

        for i, plot_data in enumerate(plots_data):
            plot = self.plots[i]
            state = plot_data.get("state")

            if state == "empty":
                plot.state = "empty"
                plot.plant = None
                plot.remaining_time = 0
                plot.total_time = 0

            elif state == "growing":
                plant_id = plot_data.get("plant_id")
                plot.state = "growing"
                plot.plant = self.get_plant_by_id(plant_id)
                plot.remaining_time = plot_data.get("remaining_time", 0)
                plot.total_time = plot_data.get("total_time", 0)

            elif state == "ready":
                plant_id = plot_data.get("plant_id")
                plot.state = "ready"
                plot.plant = self.get_plant_by_id(plant_id)
                plot.remaining_time = 0
                plot.total_time = 0

#----------------------------------------------------------------------------

    def get_plant_by_id(self, pid):
        for p in self.plants:
            if p.id == pid:
                return p
        return None

    def get_fertilizer_by_id(self, fid):
        for f in self.fertilizers:
            if f.id == fid:
                return f
        return None

    def buy_fertilizer(self, fid):
        fert = self.get_fertilizer_by_id(fid)
        if fert is None:
            return False, "Fertilizer not found"

        if self.balance < fert.price:
            return False, "Not enough money"

        self.balance -= fert.price
        self.fertilizer_inventory[fid] += 1
        return True, f"Bought {fert.name}"

    def plant_crop(self, plot_index, plant_id, fertilizer_id=None):
        plot = self.plots[plot_index]
        if plot.state != "empty":
            return False, "Plot is not empty"
        plant = self.get_plant_by_id(plant_id)
        if plant is None:
            return False, "Plant not found"
        grow_time = plant.base_grow_time
        if fertilizer_id is not None:
            fert = self.get_fertilizer_by_id(fertilizer_id)
            if fert is None:
                return False, "Fertilizer not found"
            if self.fertilizer_inventory.get(fertilizer_id, 0) <= 0:
                return False, "No such fertilizer in inventory"
            self.fertilizer_inventory[fertilizer_id] -= 1
            grow_time = int(plant.base_grow_time * fert.multiplier)
            if grow_time < 1:
                grow_time = 1
        plot.state = "growing"
        plot.plant = plant
        plot.remaining_time = grow_time
        plot.total_time = grow_time
        return True, f"Planted {plant.name} (grow time {grow_time}s)"

    def tick(self):
        just_ready=[]
        for plot in self.plots:
            if plot.state == "growing":
                if plot.remaining_time > 0:
                    plot.remaining_time -= 1
                if plot.remaining_time <= 0:
                    plot.state = "ready"
                    just_ready.append(plot)
        return just_ready

    def get_plot_stage_index(self, plot):
        if plot.state=="empty" or plot.plant is None:
            return 0
        plant = plot.plant
        if plot.total_time <= 0:
            return plant.stage_count
        progress = (plot.total_time - plot.remaining_time) / plot.total_time
        stage = int(progress * plant.stage_count)
        if stage < 1:
            stage = 1
        if stage > plant.stage_count:
            stage = plant.stage_count
        return stage

    def harvest(self, plot_index):
        plot = self.plots[plot_index]
        if plot.state != "ready" or plot.plant is None:
            return False, "Nothing to harvest"
        name = plot.plant.name
        self.barn[name] = self.barn.get(name, 0) + 1
        plot.state = "empty"
        plot.plant = None
        plot.remaining_time = 0
        plot.total_time = 0
        return True, f"Harvested 1 {name}"

    def sell_from_barn(self, plant_name):
        plant_info = None
        for p in self.plants:
            if p.name == plant_name:
                plant_info = p
                break
        if plant_info is None:
            return False, "Unknown crop"
        if self.barn.get(plant_name, 0) <= 0:
            return False, "No such crop in barn"
        self.barn[plant_name] -= 1
        self.balance += plant_info.sell_price
        return True, f"Sold 1 {plant_name} for {plant_info.sell_price}$"
