import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from separator import Separator


class StatusBar(ctk.CTkFrame):
    """Строка состояния"""
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        Separator(self).grid(row=0, column=0, sticky="we", pady=1)
        status_bar = ctk.CTkFrame(self, corner_radius=0, border_width=0, height=20,
                                  border_color="yellow", fg_color='transparent')
        status_bar.grid(row=1, column=0, sticky="we", padx=2, pady=0)

        self.stbar_pui = tk.StringVar(status_bar, '>', "stbar_pui")
        # self.stbar_file = tk.StringVar(status_bar, ' ', "stbar_file")
        ctk.CTkLabel(status_bar, textvariable=self.stbar_pui, width=200, anchor='w', padx=5).pack(
            side="left", fill="x", expand=False, padx=2, pady=0)   # pui
        # ctk.CTkLabel(status_bar, textvariable=self.stbar_file, width=1, anchor='w', padx=20).pack(
        #     side="left", fill="x", expand=False, pady=0)   # file
        ttk.Sizegrip(status_bar).pack(side='right', padx=3)

        self.progress = ctk.CTkProgressBar(status_bar, orientation="horizontal",
                                           width=350, height=12, determinate_speed=1)
        # self.progress.pack(side="right", fill="x", padx=(300, 10), ipady=0)                         # unpack
        # self.progress.set(0)      # 0 - 1
