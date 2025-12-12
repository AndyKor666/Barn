from Models.wheat import Wheat
from Models.carrot import Carrot
from Models.corn import Corn

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

        self.fertilizers = [
            Fertilizer(1, "Basic fertilizer", 10, 0.80),
            Fertilizer(2, "Super fertilizer", 20, 0.50),
        ]

        self.fertilizer_inventory = {f.id: 0 for f in self.fertilizers}
        self.barn = {}
        self.plots = [FarmPlot(i) for i in range(1, 4)]

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
            return False, "Fertilizer not found . . ."

        if self.balance < fert.price:
            return False, "Not enough money . . ."

        self.balance -= fert.price
        self.fertilizer_inventory[fid] += 1
        return True, f"Bought {fert.name}"

    def plant_crop(self, plot_index, plant_id, fertilizer_id=None):
        if plot_index < 0 or plot_index >= len(self.plots):
            return False, "Plot does not exist . . ."

        plot = self.plots[plot_index]

        if plot.state != "empty":
            return False, "Plot is not empty . . ."

        plant = self.get_plant_by_id(plant_id)
        if plant is None:
            return False, "Plant not found . . ."

        grow_time = plant.base_grow_time

        if fertilizer_id is not None:
            fert = self.get_fertilizer_by_id(fertilizer_id)
            if fert is None:
                return False, "Fertilizer not found . . ."
            if self.fertilizer_inventory.get(fertilizer_id, 0) <= 0:
                return False, "No such fertilizer in inventory . . ."

            self.fertilizer_inventory[fertilizer_id] -= 1
            grow_time = int(grow_time * fert.multiplier)
            if grow_time < 1:
                grow_time = 1

        plot.state = "growing"
        plot.plant = plant
        plot.remaining_time = grow_time
        plot.total_time = grow_time
        return True, f"Planted {plant.name} (grow time {grow_time}s)"

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

    def get_plot_stage_index(self, plot):
        if plot.state == "empty" or plot.plant is None:
            return 0

        plant = plot.plant

        if plot.total_time <= 0:
            return plant.stages

        progress = (plot.total_time - plot.remaining_time) / plot.total_time
        stage = int(progress * plant.stages)

        return max(1, min(stage, plant.stages))


    def harvest(self, plot_index):
        if plot_index < 0 or plot_index >= len(self.plots):
            return False, "Plot does not exist . . ."

        plot = self.plots[plot_index]

        if plot.state != "ready" or plot.plant is None:
            return False, "Nothing to harvest here . . ."

        name = plot.plant.name

        self.barn[name] = self.barn.get(name, 0) + 1

        plot.state = "empty"
        plot.plant = None
        plot.remaining_time = 0
        plot.total_time = 0
        plot.fert_boost = 0

        return True, f"Harvested 1 {name}"

    def sell_from_barn(self, plant_name):
        plant_info = next((p for p in self.plants if p.name == plant_name), None)
        if plant_info is None:
            return False, "Unknown crop . . ."

        if self.barn.get(plant_name, 0) <= 0:
            return False, "No such crop in barn . . ."

        self.barn[plant_name] -= 1
        self.balance += plant_info.sell_price

        return True, f"Sold 1 {plant_name} for {plant_info.sell_price}$"

    def buy_new_plot(self, dto):
        from DTO.NewField import NewFieldDTO
        if not isinstance(dto, NewFieldDTO):
            return False, "Invalid DTO"

        if len(self.plots) >= self.MAX_PLOTS:
            return False, "Maximum number of plots is reached . . ."

        price = 1000
        if dto.with_fertilizer:
            price += 1500

        if self.balance < price:
            return False, "Not enough money . . ."

        self.balance -= price

        new_plot = FarmPlot(len(self.plots) + 1)
        new_plot.fert_boost = dto.fert_boost if dto.with_fertilizer else 0

        self.plots.append(new_plot)

        return True, "New plot purchased."
