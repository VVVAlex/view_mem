#!/usr/bin/env python

import customtkinter as ctk
from tkinter import StringVar
from common import family, font_size
from separator import Separator

font = (family, font_size)


class LabHead(ctk.CTkFrame):
    """Этикетки в head"""

    def __init__(self, root,  **kwargs):
        self.root = root
        super().__init__(root, **kwargs)

        (self.glub_var, self.sh_var, self.d_var, self.t_var,
         self.scr_num_var) = (StringVar() for _ in range(5))

        # font = ctk.CTkFont(family=family, size=font_size)
        text_ = ('Глубина', 'Широта', 'Долгота', ' Время ', ' Экран ')
        # t_var_  = self.root.t_var_
        t_var_ = self.glub_var, self.sh_var, self.d_var, self.t_var, self.scr_num_var
        self.lab = []
        i = 0
        for i, j in enumerate(zip(text_, t_var_)):
            ctk.CTkLabel(self, text=j[0], font=font).grid(
                row=1, column=i, padx=1, pady=(2, 0), sticky="we")
            lb = ctk.CTkLabel(self, textvariable=j[1], font=font, fg_color=('grey85', 'grey17'))
            lb.grid(row=2, column=i, padx=1, pady=(0, 2), sticky="we")
            self.lab.append(lb)
        self.color = self.lab[0].cget('text_color')
        Separator(self).grid(row=0, column=0, columnspan=i+1, sticky="we", pady=1)
        Separator(self).grid(row=3, column=0, columnspan=i+1, sticky="we", pady=1)
        # self.set_('000.0', '00.000.00', '000.00.000', '00.00 00:00:00')

    def del_color(self, color) -> None:
        """Удалить цвет"""
        for i in self.lab[:-1]:
            i.configure(text_color=color)

