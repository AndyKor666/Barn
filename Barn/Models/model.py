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

class GameModel:
    MAX_PLOTS = 16
    PLOT_PRICE = 1000

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

        if plot.state != "empty":
            return False, "This plot is already filled :("

        plant = self.get_plant_by_id(plant_id)
        if not plant:
            return False, "Unknown plant :("

        grow_time = plant.base_grow_time

        if fertilizer_id:
            fert = self.get_fertilizer_by_id(fertilizer_id)
            if not fert or self.fertilizer_inventory[fertilizer_id] <= 0:
                return False, "No fertilizer :("
            self.fertilizer_inventory[fertilizer_id] -= 1
            grow_time = int(grow_time * fert.multiplier)
            self.stats["fertilizers_used"] += 1

        plot.state = "growing"
        plot.plant = plant
        plot.remaining_time = grow_time
        plot.total_time = grow_time

        self.stats["plants_planted"] += 1
        return True, f"Planted {plant.name} :)"

    def harvest(self, index):
        plot = self.plots[index]

        if plot.state != "ready" or not plot.plant:
            return False, "Nothing to harvest here :("

        name = plot.plant.name
        self.barn[name] = self.barn.get(name, 0) + 1
        self.stats["plants_harvested"] += 1

        plot.state = "empty"
        plot.plant = None
        plot.remaining_time = 0
        plot.total_time = 0

        return True, f"Harvested {name} :)"

    def sell_from_barn(self, name):
        if self.barn.get(name, 0) <= 0:
            return False, "No crops to sell :("

        plant = next(p for p in self.plants if p.name == name)
        self.barn[name] -= 1
        self.balance += plant.sell_price
        self.stats["sold_income"] += plant.sell_price

        return True, f"Sold {name} :)"

    def buy_fertilizer(self, fid):
        fert = self.get_fertilizer_by_id(fid)
        if not fert:
            return False, "Unknown fertilizer :("

        if self.balance < fert.price:
            return False, "Not enough money :("

        self.balance -= fert.price
        self.fertilizer_inventory[fid] += 1
        return True, f"{fert.name} bought :)"

    def buy_new_plot(self, dto=None):
        if len(self.plots) >= self.MAX_PLOTS:
            return False, "Maximum amount of plots reached :("

        if self.balance < self.PLOT_PRICE:
            return False, "Not enough money :("

        self.balance -= self.PLOT_PRICE
        self.plots.append(FarmPlot(len(self.plots)))
        self.stats["plots_bought"] += 1

        return True, "New plot bought :)"


    def tick(self):
        ready = []
        for plot in self.plots:
            if plot.state == "growing":
                plot.remaining_time -= 1
                if plot.remaining_time <= 0:
                    plot.state = "ready"
                    ready.append(plot)
        return ready


    def get_plot_stage_index(self, plot):
        if not plot or not plot.plant:
            return 1

        if plot.state == "ready":
            return plot.plant.stages

        total = plot.total_time
        remaining = plot.remaining_time

        if total <= 0:
            return 1

        elapsed = total - remaining
        part = total / plot.plant.stages
        stage = int(elapsed / part) + 1

        return max(1, min(plot.plant.stages, stage))
