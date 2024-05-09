#!/usr/bin/env python

import customtkinter as ctk
from head_label import LabHead


class Head(ctk.CTkFrame):
    """Информационный верхний фрейм"""

    def __init__(self, root,  **kwargs):
        self.root = root
        super().__init__(root, **kwargs)

        self.lab_heat = LabHead(self)
        self.lab_heat.grid(sticky="nsew")
        self.lab_heat.columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.lab = self.lab_heat.lab
        self.color = self.lab_heat.color

        self.set_('000.0', '', '', '00.00 00:00:00')
        fg_color = self.lab[0].cget('fg_color')
        self.lab_heat.del_color(fg_color)

    # @staticmethod
    # def dop_gradus(st: str) -> str:
    #     """Вставляем знак градуса и минуту"""
    #     if st:
    #         d = st.split()
    #         d[0] = f'{d[0]}{0xB0:c} '
    #         d[1] = f'{d[1]}{0xB4:c} '
    #         st = ''.join(d)
    #     return st

    def set_glub(self, gl: str) -> None:
        """Установка глубины"""
        self.lab_heat.glub_var.set(f'{gl}')

    def set_scr_num(self, scr_num: str) -> None:
        """Установка номера экрана"""
        self.lab_heat.scr_num_var.set(f'{scr_num}')

    def get_scr_num(self) -> str:
        """Возвращение номера экрана"""
        return self.lab_heat.scr_num_var.get()

    # def set_scala(self, scala: str) -> None:
    #     """Установка шкалы"""
    #     self.scala_var.set(f'{scala}')

    def set_sh(self, sh: str) -> None:
        """Установка широты"""
        # sh = self.dop_gradus(sh)
        self.lab_heat.sh_var.set(f'{sh}')

    def set_d(self, d: str) -> None:
        """Установка долготы"""
        # d = self.dop_gradus(d)
        self.lab_heat.d_var.set(f'{d}')

    def set_t(self, t: str) -> None:
        """Установка времени"""
        self.lab_heat.t_var.set(f'{t}')

    def set_(self, *arg) -> None:
        """Обновляем StringVar arg=(глубина, широта, долгота, время, экран)"""
        self.set_glub(arg[0])
        self.set_sh(arg[1])
        self.set_d(arg[2])
        self.set_t(arg[3])
        # self.set_scr_num(arg[4])
        # self.set_scala(arg[5])
