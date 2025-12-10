import os
import json

class ResourceService:
    SAVE_FILE = "save.json"
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ASSETS_DIR = os.path.join(BASE_DIR, "assets")
    _resources = {
        "empty": os.path.join(ASSETS_DIR, "empty.png"),

        "corn_1": os.path.join(ASSETS_DIR, "corn_1.png"),
        "corn_2": os.path.join(ASSETS_DIR, "corn_2.png"),
        "corn_3": os.path.join(ASSETS_DIR, "corn_3.png"),
        "corn_4": os.path.join(ASSETS_DIR, "corn_4.png"),

        "carrot_1": os.path.join(ASSETS_DIR, "carrot_1.png"),
        "carrot_2": os.path.join(ASSETS_DIR, "carrot_2.png"),
        "carrot_3": os.path.join(ASSETS_DIR, "carrot_3.png"),
        "carrot_4": os.path.join(ASSETS_DIR, "carrot_4.png"),

        "wheat_1": os.path.join(ASSETS_DIR, "wheat_1.png"),
        "wheat_2": os.path.join(ASSETS_DIR, "wheat_2.png"),
        "wheat_3": os.path.join(ASSETS_DIR, "wheat_3.png"),
        "wheat_4": os.path.join(ASSETS_DIR, "wheat_4.png"),
    }

    @staticmethod
    def get_item(key: str) -> str:
        print("LOADING:", key)
        if key in ResourceService._resources:
            path = ResourceService._resources[key]
            print("PATH:", path)
            if os.path.exists(path):
                return path

        if "_" in key:
            prefix = key.split("_")[0]

            candidates = [
                k for k in ResourceService._resources
                if k.startswith(prefix + "_")
            ]
            if candidates:
                return ResourceService._resources[candidates[-1]]
        return None

    @staticmethod
    def save_game(model):
        data = {
            "balance": model.balance,
            "barn": model.barn,
            "fertilizers": model.fertilizer_inventory,
            "plots": []
        }
        for plot in model.plots:
            if plot.state == "empty":
                data["plots"].append({"state": "empty"})
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

        with open(ResourceService.SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_game(model):
        if not os.path.exists(ResourceService.SAVE_FILE):
            return
        try:
            with open(ResourceService.SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            return

        model.balance = data.get("balance", 50)
        model.barn = data.get("barn", {})

        model.fertilizer_inventory = {
            int(k): v for k, v in data.get("fertilizers", {}).items()
        }
        plots = data.get("plots", [])

        for i, plot_data in enumerate(plots):
            plot = model.plots[i]
            state = plot_data.get("state")

            if state == "empty":
                plot.state = "empty"
                plot.plant = None
                plot.remaining_time = 0
                plot.total_time = 0

            elif state == "growing":
                plant_id = plot_data.get("plant_id")
                plot.state = "growing"
                plot.plant = model.get_plant_by_id(plant_id)
                plot.remaining_time = plot_data.get("remaining_time", 0)
                plot.total_time = plot_data.get("total_time", 0)

            elif state == "ready":
                plant_id = plot_data.get("plant_id")
                plot.state = "ready"
                plot.plant = model.get_plant_by_id(plant_id)
                plot.remaining_time = 0
                plot.total_time = 0
