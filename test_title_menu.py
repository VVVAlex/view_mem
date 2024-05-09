import customtkinter as ctk
from menu_bar import CTkMenuBar
from title_menu_win import CTkTitleMenu
from dropdown_menu import CustomDropdownMenu
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from common import load_image, im_dict
from ctk_popupmenu import CTkPopupMenu

ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.after(300, lambda: self.iconbitmap("setup.ico"))
        self.TkdndVersion = TkinterDnD._require(self)
        self.after(300, lambda: self.iconbitmap("setup.ico"))
        self.title("")
        self.s = ttk.Style()
        self.s.theme_use("clam")

        ctk.set_appearance_mode("Dark")
        ctk.set_appearance_mode("Light")

        # xx = ctk.ThemeManager.theme["CTkButton"]["hover_color"]
        # print(xx)

        self.create_menu()
        # ctk.set_appearance_mode("Dark")

        self.frame = ctk.CTkFrame(master=self, corner_radius=0, border_width=1, width=400, height=400,
                                  border_color='red')
        # self.frame.pack(fill='both', expand=True)
        self.frame.grid()

        self.frame.grid_columnconfigure(0, weight=100)
        self.frame.grid_rowconfigure(0, weight=100)

        self.frame_top = ctk.CTkFrame(
            master=self.frame, corner_radius=0, border_width=0, border_color="yellow", height=30, width=400,
        )
        self.frame_top.grid(row=0, padx=(2, 2), pady=(2, 0), sticky="we")
        self.frame_main = ctk.CTkFrame(
            master=self.frame, corner_radius=0, border_width=0, border_color="red",
        )
        self.frame_main.grid(row=1, sticky="nsew", padx=(2, 2), pady=1)

        self.frame_main.grid_rowconfigure(0, weight=1)
        self.frame_main.grid_columnconfigure(0, weight=1)

        self.frame_bottom = ctk.CTkFrame(
            master=self.frame, corner_radius=0, border_width=0, border_color="green", height=30
        )
        self.frame_bottom.grid(row=2, padx=(2, 2), pady=2, sticky="we")

        # self.frame_bottom.grid_rowconfigure(0, weight=1)
        # self.frame_bottom.grid_columnconfigure(0, weight=1)

        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.open_log_drop)

        self.pop_up(self.frame_main)
        # self.menu.grid()

    def create_menu(self) -> None:
        """Создание меню"""
        self.menu = CTkMenuBar(self)
        # self.menu = CTkTitleMenu(self, padx=10, x_offset=50, title_bar_color='yellow')
        self.menu.grid(sticky="w", padx=5)
        button_1 = self.menu.add_cascade("Файл", hover_color=('#77A1BF', '#14375e'))
        button_2 = self.menu.add_cascade("Пуи")
        dropdown1 = CustomDropdownMenu(widget=button_1, width=120)
        dropdown1.add_option(option="Просмотр PDF", image=im_dict['pdf'], command=self.dark)
        dropdown1.add_option(option="Печать", command=self.light)
        dropdown1.add_separator()
        dropdown1.add_option(option="Выход", command=self.on_closing)
        dropdown2 = CustomDropdownMenu(widget=button_2, width=140)

    @staticmethod
    def pop_up(frame):
        pp = CTkPopupMenu(frame, width=160)
        pp.configure(
            values=({'text': 'Чтение ПУИ', 'command': lambda: None, "image": im_dict['pui']},
                    None,
                    {'text': 'Выход', 'command': lambda: None, 'image': im_dict['exit']}))

    def dark(self):
        ctk.set_appearance_mode("Dark")
        # self.menu.change_dimension()
        self.geom()

    def light(self):
        ctk.set_appearance_mode("Light")
        # self.menu.change_dimension()
        self.geom()

    def geom(self):
        geometry_str = self.geometry()
        tmp = geometry_str.split('x')
        width = tmp[0]
        tmp2 = tmp[-1].split('+')
        height = tmp2[0]
        x = tmp2[1]
        y = str(int(tmp2[2]) + 1)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def open_log_drop(self, event) -> None:
        """Открытие файла перетаскиванием"""
        pass

    def on_closing(self, arg=None) -> None:
        """Выход"""
        raise SystemExit()


if __name__ == "__main__":
    app = App()
    app.mainloop()
