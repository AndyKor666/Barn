from Models.mission_model import MissionModel
from Models.corn import Corn
from Models.carrot import Carrot
from Models.wheat import Wheat

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
        self.fert_boost = 0

class GameModel:
    MAX_PLOTS = 16
    def __init__(self):
        self.balance = 50
        self.plants = [Corn(), Carrot(), Wheat()]
        self.plots = [FarmPlot(i) for i in range(3)]

        self.fertilizers = [
            Fertilizer(1, "Basic fertilizer", 10, 0.8),
            Fertilizer(2, "Super fertilizer", 20, 0.5)
        ]

        self.fertilizer_inventory = {f.id: 0 for f in self.fertilizers}
        self.barn = {}

        self.stats = {
            "plants_planted": 0,
            "plants_harvested": 0,
            "fertilizers_used": 0,
            "plots_bought": 0,
            "sold_income": 0
        }

        self.mission_model = MissionModel()

    def get_plant_by_id(self, pid):
        return next((p for p in self.plants if p.id == pid), None)

    def get_fertilizer_by_id(self, fid):
        return next((f for f in self.fertilizers if f.id == fid), None)

    def plant_crop(self, index, plant_id, fertilizer_id=None):
        plot = self.plots[index]
        plant = self.get_plant_by_id(plant_id)

        time = plant.base_grow_time

        if fertilizer_id:
            fert = self.get_fertilizer_by_id(fertilizer_id)
            if self.fertilizer_inventory[fertilizer_id] <= 0:
                return False, "No fertilizer :("

            self.fertilizer_inventory[fertilizer_id] -= 1
            time = int(time * fert.multiplier)
            plot.fert_boost = fert.multiplier
            self.stats["fertilizers_used"] += 1

        plot.state = "growing"
        plot.plant = plant
        plot.remaining_time = time
        plot.total_time = time

        self.stats["plants_planted"] += 1
        return True, f"Planted {plant.name}"

    def harvest(self, index):
        plot = self.plots[index]
        name = plot.plant.name

        self.barn[name] = self.barn.get(name, 0) + 1
        self.stats["plants_harvested"] += 1

        plot.state = "empty"
        plot.plant = None
        plot.remaining_time = 0
        plot.total_time = 0
        plot.fert_boost = 0

        return True, f"Harvested {name}"

    def sell_from_barn(self, name):
        plant = next(p for p in self.plants if p.name == name)
        self.barn[name] -= 1
        self.balance += plant.sell_price
        self.stats["sold_income"] += plant.sell_price
        return True, f"Sold {name}"

    def buy_fertilizer(self, fid):
        fert = self.get_fertilizer_by_id(fid)
        if self.balance < fert.price:
            return False, "Not enough money :("

        self.balance -= fert.price
        self.fertilizer_inventory[fid] += 1
        return True, "Fertilizer bought :)"

    def buy_new_plot(self, dto=None):
        if len(self.plots) >= self.MAX_PLOTS:
            return False, "Maximum amount of plots reached :("

        if self.balance < 1000:
            return False, "Not enough money :("

        self.balance -= 1000
        self.plots.append(FarmPlot(len(self.plots)))
        self.stats["plots_bought"] += 1
        return True, "New plot bought :)"

    def tick(self):
        ready = []
        for p in self.plots:
            if p.state == "growing":
                p.remaining_time -= 1
                if p.remaining_time <= 0:
                    p.state = "ready"
                    ready.append(p)
        return ready

    def get_plot_stage_index(self, plot):
        if plot.state != "growing":
            return plot.plant.stages

        elapsed = plot.total_time - plot.remaining_time
        part = plot.total_time / plot.plant.stages
        return max(1, min(plot.plant.stages, int(elapsed / part) + 1))
