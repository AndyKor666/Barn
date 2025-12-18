import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class GameView:
    def __init__(self, root, max_plots=16):
        self.root = root
        self.root.title("Farm")
        self.root.geometry("950x600")
        self.root.configure(bg="#f4f4f4")

        self.max_plots = max_plots
        self._plot_images = [None] * max_plots
        top_frame = tk.Frame(root, bg="#f4f4f4")
        top_frame.pack(fill="x", pady=10)

        self.balance_label = tk.Label(
            top_frame, text="Balance: $0", font=("Consolas", 14, "bold"),
            bg="#f4f4f4"
        )
        self.balance_label.pack(side="left", padx=20)

        self.message_label = tk.Label(
            top_frame, text="", font=("Consolas", 12, "italic"),
            bg="#f4f4f4", fg="#555555"
        )
        self.message_label.pack(side="right", padx=20)

        farm_frame = tk.LabelFrame(
            root, text="Farm", font=("Consolas", 12, "bold"),
            bg="#f4f4f4"
        )
        farm_frame.pack(side="left", padx=10, pady=5, fill="y")
        self.canvas = tk.Canvas(
            farm_frame, bg="#f4f4f4", highlightthickness=0, width=210
        )
        self.canvas.pack(side="left", fill="y", expand=False)

        self.scrollbar = tk.Scrollbar(
            farm_frame, orient="vertical", command=self.canvas.yview
        )
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.inner_frame = tk.Frame(self.canvas, bg="#f4f4f4")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        ))

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.plot_frames = []
        self.plot_status_labels = []
        self.plot_buttons = []
        self.plot_image_labels = []

        for i in range(max_plots):
            frame = tk.Frame(self.inner_frame, bg="#ffffff", bd=1, relief="solid")
            frame.pack(padx=10, pady=5, fill="x")

            title = tk.Label(
                frame, text=f"Plot {i + 1}",
                font=("Consolas", 12, "bold"),
                bg="#ffffff"
            )
            title.pack(pady=3)

            img_label = tk.Label(frame, bg="#ffffff")
            img_label.pack(pady=3)

            status_label = tk.Label(
                frame, text="Locked", font=("Consolas", 11),
                bg="#ffffff"
            )
            status_label.pack(pady=3)

            btn = tk.Button(
                frame, text="Locked", font=("Consolas", 11),
                bg="#e0e0e0", state="disabled"
            )
            btn.pack(pady=3, fill="x")

            self.plot_frames.append(frame)
            self.plot_status_labels.append(status_label)
            self.plot_buttons.append(btn)
            self.plot_image_labels.append(img_label)

        right_frame = tk.Frame(root, bg="#f4f4f4")
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

        plant_box = tk.LabelFrame(
            right_frame, text="Plant selection",
            font=("Consolas", 11, "bold"), bg="#f4f4f4"
        )
        plant_box.pack(fill="x", pady=5)

        self.plant_combo = ttk.Combobox(
            plant_box, state="readonly", font=("Consolas", 11),
            width=25
        )
        self.plant_combo.pack(padx=10, pady=5)

        fert_box = tk.LabelFrame(
            right_frame, text="Fertilizer (from inventory)",
            font=("Consolas", 11, "bold"), bg="#f4f4f4"
        )
        fert_box.pack(fill="x", pady=5)

        self.fert_combo = ttk.Combobox(
            fert_box, state="readonly", font=("Consolas", 11),
            width=25
        )
        self.fert_combo.pack(padx=10, pady=5)

        self.fert_inv_label = tk.Label(
            fert_box, text="Inventory:", font=("Consolas", 10),
            bg="#f4f4f4", justify="left"
        )
        self.fert_inv_label.pack(pady=5, padx=10, anchor="w")

        btn_box = tk.Frame(right_frame, bg="#f4f4f4")
        btn_box.pack(fill="x", pady=10)

        self.open_shop_button = tk.Button(
            btn_box, text="Open shop", font=("Consolas", 11),
            bg="#e0e0e0"
        )
        self.open_shop_button.pack(side="left", padx=10)

        self.open_barn_button = tk.Button(
            btn_box, text="Open barn", font=("Consolas", 11),
            bg="#e0e0e0"
        )
        self.open_barn_button.pack(side="left", padx=10)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _load_image(self, img_path, size=(96, 96)):
        if not img_path or not os.path.exists(img_path):
            return None
        try:
            img = Image.open(img_path)
            img = img.resize(size)
            return ImageTk.PhotoImage(img)
        except:
            return None

    def set_balance(self, balance):
        self.balance_label.config(text=f"Balance: ${balance}")

    def set_message(self, msg):
        self.message_label.config(text=msg)

    def update_plot(self, index, state_text, img_path=None,
                    button_text=None, button_state="normal"):

        if index < 0 or index >= self.max_plots:
            return

        self.plot_status_labels[index].config(text=state_text)

        pic = self._load_image(img_path)
        self._plot_images[index] = pic

        if pic:
            self.plot_image_labels[index].config(image=pic)
        else:
            self.plot_image_labels[index].config(image="")

        if button_text is not None:
            self.plot_buttons[index].config(
                text=button_text, state=button_state
            )

    def set_plant_options(self, names):
        self.plant_combo["values"] = names
        if names:
            self.plant_combo.current(0)

    def set_fert_options(self, names):
        self.fert_combo["values"] = ["None"] + names
        self.fert_combo.current(0)

    def update_fertilizer_inventory(self, text):
        self.fert_inv_label.config(text="Inventory:\n" + text)

class ShopWindow(tk.Toplevel):
    def __init__(self, root, model, controller):
        super().__init__(root)
        self.title("Shop")
        self.geometry("450x550")
        self.configure(bg="#DFDFDF")
        self.model = model
        self.controller = controller

        title = tk.Label(self, text="Shop", font=("Consolas", 14, "bold"), bg="#DFDFDF")
        title.pack(pady=10)

        self.balance_label = tk.Label(self, text="", font=("Consolas", 12), bg="#DFDFDF")
        self.balance_label.pack(pady=5)

        fert_frame = tk.LabelFrame(self, text="Fertilizers",
                                   font=("Consolas", 11, "bold"),
                                   bg="#DFDFDF")
        fert_frame.pack(fill="x", padx=10, pady=10)

        for f in self.model.fertilizers:
            row = tk.Frame(fert_frame, bg="#DFDFDF")
            row.pack(fill="x", pady=3)

            lbl = tk.Label(row, text=f"{f.name} - ${f.price}",
                           font=("Consolas", 10), bg="#DFDFDF")
            lbl.pack(side="left", padx=5)

            btn = tk.Button(row, text="Buy",
                            font=("Consolas", 10), bg="#e0e0e0",
                            command=lambda fid=f.id: self.controller.shop_buy_fert(fid))
            btn.pack(side="right", padx=5)

        plot_frame = tk.LabelFrame(self, text="New plots",
                                   font=("Consolas", 11, "bold"),
                                   bg="#DFDFDF")
        plot_frame.pack(fill="x", padx=10, pady=10)

        info = tk.Label(plot_frame,
                        text="Land price: $1000\nWith fertilizer: +$1500",
                        font=("Consolas", 9),
                        bg="#DFDFDF", justify="left")
        info.pack(pady=5, padx=5, anchor="w")

        btn_row = tk.Frame(plot_frame, bg="#DFDFDF")
        btn_row.pack(fill="x", pady=5)

        self.btn_buy_plot = tk.Button(btn_row, text="Buy new plot ($1000)",
                                      font=("Consolas", 10), bg="#e0e0e0",
                                      command=lambda: self.controller.shop_buy_new_plot(False))
        self.btn_buy_plot.pack(side="left", padx=5)

        self.btn_buy_plot_fert = tk.Button(btn_row, text="Buy plot + fertilizer ($2500)",
                                           font=("Consolas", 10), bg="#e0e0e0",
                                           command=lambda: self.controller.shop_buy_new_plot(True))
        self.btn_buy_plot_fert.pack(side="left", padx=5)

        sell_frame = tk.LabelFrame(self, text="Sell crops",
                                   font=("Consolas", 11, "bold"),
                                   bg="#DFDFDF")
        sell_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.barn_listbox = tk.Listbox(sell_frame, font=("Consolas", 10), height=6)
        self.barn_listbox.pack(padx=5, pady=5, fill="both", expand=True)

        self.sell_button = tk.Button(sell_frame, text="Sell selected",
                                     font=("Consolas", 10), bg="#e0e0e0",
                                     command=self._on_sell)
        self.sell_button.pack(pady=5)

        self.refresh()

    def refresh(self):
        self.balance_label.config(text=f"Balance: ${self.model.balance}")
        self.barn_listbox.delete(0, "end")

        for name, count in sorted(self.model.barn.items()):
            if count > 0:
                self.barn_listbox.insert("end", f"{name} x{count}")

    def _on_sell(self):
        selection = self.barn_listbox.curselection()
        if not selection:
            self.controller.set_message("Select a crop to sell . . .")
            return

        line = self.barn_listbox.get(selection[0])
        name, count = line.split(" x")
        count = int(count)

        ok, msg = self.controller.shop_sell_crop(name, count)
        self.controller.set_message(msg)
        self.controller.refresh_all()
        self.refresh()


class BarnWindow(tk.Toplevel):
    def __init__(self, root, model, controller):
        super().__init__(root)
        self.title("Barn")
        self.geometry("350x300")
        self.configure(bg="#DFDFDF")
        self.model = model
        self.controller = controller

        title = tk.Label(self, text="Barn Storage",
                         font=("Consolas", 14, "bold"), bg="#DFDFDF")
        title.pack(pady=10)

        self.listbox = tk.Listbox(self, font=("Consolas", 11), height=10)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh()

    def refresh(self):
        self.listbox.delete(0, "end")
        for name, count in sorted(self.model.barn.items()):
            if count > 0:
                self.listbox.insert("end", f"{name} x{count}")
