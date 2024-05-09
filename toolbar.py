import customtkinter as ctk
import tkinter as tk
from ctk_tooltip import CTkToolTip as ToolTip
from common import load_image, im_dict
from separator import Separator


class ToolBar(ctk.CTkFrame):
    """Панель инструментов"""
    def __init__(self, root, **kwargs):
        self.root = root
        super().__init__(root, **kwargs)

        self.b = []
        im_korabl = load_image('korab.png', 'korab2.png', size=(48, 24))

        fg = 'transparent'
        hc = ["grey75", "grey25"]
        width = 2
        row = 0
        self.toolbar = ctk.CTkFrame(self, corner_radius=0, border_width=0, fg_color=fg)
        Separator(self.toolbar).pack(fill='x')
        height = self.root.height - 8
        bar_left = ctk.CTkFrame(self.toolbar, corner_radius=0, border_width=0, fg_color=fg, height=height)
        self.bar_right = ctk.CTkFrame(self.toolbar, corner_radius=0, border_width=0, fg_color=fg, height=height)
        im = im_dict
        j = 0
        for image, tip, command in (
                (im['exit'], 'Выход', root.on_closing),
                (None, None, None),
                (im['pui'], 'Чтение из ПУИ', root.read_pui),
                (im['mem'], 'Просмотр памяти', root.view_mem),
                (None, None, None),
                (im['print'], 'Печать', root.print_pdf),
                (im['pdf'], 'Просмотр PDF', root.view_pdf),
                (None, None, None),
                (im['link'], 'Домашняя страница', root.show_web_page),
                (None, None, None),
        ):
            j += 1
            try:
                if image is None:
                    Separator(bar_left, orient="vertical").grid(row=row, column=j, sticky="ns", padx=2, pady=1)
                else:
                    bt = ctk.CTkButton(bar_left, image=image, compound="left", text='',
                                       cursor="hand2", fg_color=fg,  hover_color=hc,
                                       width=width, command=command)
                    bt.grid(row=row, column=j, padx=2)
                    ToolTip(bt, message=tip)
                    self.b.append(bt)
            except tk.TclError as err:
                pass
        self.b[3].configure(state='disabled')
        self.b[4].configure(state='disabled')
        self.br = []
        j = 0
        for image, tip, command in (
                (None, None, None),
                (im['grid'], 'Сетка', root.grid_on_off),
                (im['dno'], 'Подсветка дна', root.dno_on_off),
                (im['avto'], 'Автомасштаб', root.avto_on_off),
                (None, None, None),
                (im['left'], 'Следующий экран', root.next),
                (im['right'], 'Предыдущий экран', root.prev),
                (im['up'], 'Увеличить масштаб', root.up),
                (im['down'], 'Уменьшить масштаб', root.down),
                (None, None, None),
                (im['expand'], 'Вся память', root.full),
                (None, None, None),
                (im['number'], 'Перейти на экран', root.board.go_screen),
                (None, None, None)
        ):
            j += 1
            try:
                if image is None:
                    Separator(self.bar_right, orient="vertical").grid(row=row, column=j, sticky="ns", padx=2, pady=1)
                else:
                    bt = ctk.CTkButton(self.bar_right, image=image, compound="left", text='',
                                       cursor="hand2", fg_color=fg, hover_color=hc,
                                       width=width, command=command)
                    bt.grid(row=row, column=j, padx=(2, 0))
                    ToolTip(bt, message=tip)
                    self.br.append(bt)          # [2] масштаб root.avto_on_off()
            except tk.TclError:
                pass
        bar_left.pack(side='left', fill='x')
        # self.bar_right.pack(side='left', padx=40)                         # unpack
        self.toolbar.grid(sticky="nsew")
        ctk.CTkLabel(master=self.toolbar, image=im_korabl, text='',
                     fg_color=fg).pack(side='right', padx=10, pady=5)
