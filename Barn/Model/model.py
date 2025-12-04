import os
SAVE_FILE = "save.txt"

class Plant:
    def __init__(self, pid, name, base_grow_time, sell_price, stage_count, image_prefix):
        self.id=pid
        self.name=name
        self.base_grow_time=base_grow_time
        self.sell_price=sell_price
        self.stage_count=stage_count
        self.image_prefix=image_prefix

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

        self.plants = [
            Plant(1, "Corn", 12, 20, 4, "corn"),
            Plant(2, "Carrot", 6, 8, 4, "carrot"),
            Plant(3, "Wheat", 8, 12, 4, "wheat"),
        ]

        self.fertilizers = [
            Fertilizer(1, "Basic Fertilizer",  10, 0.8),
            Fertilizer(2, "Super Fertilizer",  20, 0.5),
        ]

        self.fertilizer_inventory = {}
        for f in self.fertilizers:
            self.fertilizer_inventory[f.id] = 0

        self.barn = {}
        self.plots = [FarmPlot(i) for i in range(1, 4)]


#----------------------------------------------------------------------------

    def save_game(self):
        lines=[]
        lines.append(f"Balance is {self.balance}$")
        barn_str=",".join([f"{name}:{count}" for name, count in self.barn.items()])
        if self.barn:
            barn_str=",".join(f"{name}:{count}" for name, count in self.barn.items())
            lines.append(f"Barn has {barn_str}.")
        else:
            lines.append("Barn is empty.")
        fert_str=",".join([f"{fid}:{count}" for fid, count in self.fertilizer_inventory.items()])
        lines.append(f"Fertilizers -> {fert_str}")
        for i, p in enumerate(self.plots):
            if p.state == "empty":
                lines.append(f"Plot {i+1}: empty")
            elif p.state == "growing":
                lines.append(f"Plot {i+1}: growing, plant: {p.plant.id}, remaining: {p.remaining_time}")
            elif p.state == "ready":
                lines.append(f"Plot {i+1}: ready, plant: {p.plant.id}")
        with open(SAVE_FILE, "w") as f:
            f.write("\n".join(lines))

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            return
        try:
            with open(SAVE_FILE, "r") as f:
                lines = f.read().splitlines()
        except:
            return

        data={}
        for line in lines:
            if "=" in line:
                key, value = line.split("=", 1)
                data[key] = value
        self.balance = int(data.get("balance", 0))
        barn_raw = data.get("barn", "")
        self.barn = {}
        if barn_raw:
            for item in barn_raw.split(","):
                if ":" in item:
                    name, count = item.split(":")
                    self.barn[name] = int(count)
        fert_raw = data.get("fertilizers", "")
        self.fertilizer_inventory = {}
        if fert_raw:
            for item in fert_raw.split(","):
                if ":" in item:
                    fid, count = item.split(":")
                    self.fertilizer_inventory[int(fid)] = int(count)
        for i in range(len(self.plots)):
            key=f"plot{i}"
            if key not in data:
                continue
            val=data[key]
            if val == "empty":
                self.plots[i].state = "empty"
                self.plots[i].plant = None
                self.plots[i].remaining_time = 0
            else:
                parts = val.split(",")
                state = parts[0]
                self.plots[i].state = state
                plant_id = None
                remaining = 0
                for p in parts[1:]:
                    if p.startswith("plant="):
                        plant_id = int(p.split("=")[1])
                    elif p.startswith("remaining="):
                        remaining = int(p.split("=")[1])
                if plant_id is not None:
                    plant = next(pl for pl in self.plants if pl.id == plant_id)
                    self.plots[i].plant = plant
                self.plots[i].remaining_time = remaining

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
        self.fertilizer_inventory.setdefault(fid, 0)
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