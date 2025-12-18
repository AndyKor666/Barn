from Models.wheat import Wheat
from Models.carrot import Carrot
from Models.corn import Corn
from Models.mission_model import MissionModel, Mission

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
        self.mission_model = MissionModel()
        self.plants = [Corn(), Carrot(), Wheat()]
        self.fertilizers = [
            Fertilizer(1, "Basic fertilizer", 10, 0.8),
            Fertilizer(2, "Super fertilizer", 20, 0.5),
        ]
        self.fertilizer_inventory = {f.id: 0 for f in self.fertilizers}
        self.barn = {}
        self.plots = [FarmPlot(i) for i in range(1, 4)]

        self._init_missions()

    def _init_missions(self):
        self.mission_model.add_mission(Mission(
            mid=1,
            title="First harvest",
            description="Harvest any crop once",
            reward=50,
            condition=lambda m: sum(m.barn.values()) >= 1
        ))
        self.mission_model.add_mission(Mission(
            mid=2,
            title="Farmer",
            description="Harvest 5 crops",
            reward=150,
            condition=lambda m: sum(m.barn.values()) >= 5
        ))
        self.mission_model.add_mission(Mission(
            mid=3,
            title="Businessman",
            description="Earn $200",
            reward=200,
            condition=lambda m: m.balance >= 200
        ))
    def get_plant_by_id(self, pid):
        return next((p for p in self.plants if p.id == pid), None)

    def get_fertilizer_by_id(self, fid):
        return next((f for f in self.fertilizers if f.id == fid), None)

    def plant_crop(self, plot_index, plant_id, fertilizer_id=None):
        plot = self.plots[plot_index]
        if plot.state != "empty":
            return False, "Plot is not empty"

        plant = self.get_plant_by_id(plant_id)
        grow_time = plant.base_grow_time

        if fertilizer_id:
            fert = self.get_fertilizer_by_id(fertilizer_id)
            if self.fertilizer_inventory[fert.id] <= 0:
                return False, "No fertilizer"
            self.fertilizer_inventory[fert.id] -= 1
            grow_time = max(1, int(grow_time * fert.multiplier))

        plot.state = "growing"
        plot.plant = plant
        plot.remaining_time = grow_time
        plot.total_time = grow_time
        return True, f"Planted {plant.name}"

    def harvest(self, plot_index):
        plot = self.plots[plot_index]
        if plot.state != "ready":
            return False, "Nothing to harvest :("

        name = plot.plant.name
        self.barn[name] = self.barn.get(name, 0) + 1

        plot.state = "empty"
        plot.plant = None
        plot.remaining_time = 0
        plot.total_time = 0
        return True, f"Harvested {name}"

    def sell_from_barn(self, plant_name):
        if self.barn.get(plant_name, 0) <= 0:
            return False, "No crop"
        plant = next(p for p in self.plants if p.name == plant_name)
        self.barn[plant_name] -= 1
        self.balance += plant.sell_price

        return True, f"Sold {plant_name}"
    def tick(self):
        just_ready = []
        for plot in self.plots:
            if plot.state == "growing":
                speed = 2 if plot.fert_boost > 0 else 1
                plot.remaining_time -= speed
                if plot.fert_boost > 0:
                    plot.fert_boost -= 1
                if plot.remaining_time <= 0:
                    plot.state = "ready"
                    plot.remaining_time = 0
                    just_ready.append(plot)
        return just_ready

    def buy_new_plot(self, dto):
        from DTO.NewField import NewFieldDTO

        if not isinstance(dto, NewFieldDTO):
            return False, "Invalid data :("

        if len(self.plots) >= self.MAX_PLOTS:
            return False, "Maximum number of plots reached :("
        price = 1000
        if dto.with_fertilizer:
            price += 1500

        if self.balance < price:
            return False, "Not enough money :("
        self.balance -= price

        new_plot = FarmPlot(len(self.plots) + 1)
        new_plot.fert_boost = dto.fert_boost if dto.with_fertilizer else 0
        self.plots.append(new_plot)

        return True, "New plot purchased :)"

    def buy_fertilizer(self, fid):
        fert = self.get_fertilizer_by_id(fid)
        if fert is None:
            return False, "Fertilizer not found :("

        if self.balance < fert.price:
            return False, "Not enough money :("

        self.balance -= fert.price
        self.fertilizer_inventory[fid] += 1

        return True, f"Bought {fert.name} :)"
