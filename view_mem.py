
import customtkinter as ctk
from ctkmessagebox import CTkMessagebox as Box
from title_menu_win import CTkTitleMenu
from dropdown_menu import CustomDropdownMenu
from ctk_popupmenu import CTkPopupMenu
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD  # ,DND_ALL
from common import im_dict, config, write_config, family, font_size_16
from ctk_tooltip import CTkToolTip as ToolTip
from toolbar import ToolBar
from head import Head
from screen import Fild
from scan import RS232
from statusbar import StatusBar
from pdf import Pdf
# from pathlib import Path

# Width = 920
# Height = 700
Width = config.getint('Size', 'width')
Height = config.getint('Size', 'height')
# ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
scheme = config.get('Sys', 'scheme')
ctk.set_default_color_theme(scheme)
# ctk.set_default_color_theme("dark-blue")     # Themes: "blue", "green"

trace = print if False else lambda *x: None

font = (family, font_size_16)


class App(ctk.CTk, TkinterDnD.DnDWrapper):
    """Корневой класс приложения"""

    WIDTH = 1040  # 1340
    HEIGHT = 750  #

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename = None
        self.scan_pui = None
        self.byte_size = 52224
        self.port = False
        self.TkdndVersion = TkinterDnD._require(self)
        # font = ctk.CTkFont(family=family, size=size)

        self.after(300, lambda: self.iconbitmap("setup.ico"))
        self.title("")
        self.geometry(f"{Width}x{Height}+100+50")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.minsize(1080, 680)
        self.s = ttk.Style()
        self.s.theme_use("clam")  # default
        appearance_mode = config.get('Sys', 'app_mode')
        ctk.set_appearance_mode(appearance_mode)
        self.dropdown = []
        self.create_menu()
        self._change_appearance_mode(appearance_mode)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.view_data = None

        self.height = 35
        self.board = Fild(self)
        self.toolbar = ToolBar(self)
        self.head = Head(self)
        self.stbar = StatusBar(self)

        self.toolbar.grid(row=0, padx=2, pady=(2, 0), sticky="we")
        self.head.grid(row=1, sticky="we")
        self.board.grid(row=2, sticky="nsew")
        self.stbar.grid(row=3, sticky="we")

        self.toolbar.columnconfigure(0, weight=1)
        self.stbar.columnconfigure(0, weight=1)
        self.head.columnconfigure(0, weight=1)
        self.board.columnconfigure(0, weight=1)
        self.board.rowconfigure(3, weight=1)

        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.open_log_drop)

        self.avtoscale = config.getboolean('Preferens', 'avto')
        var = 'on' if self.avtoscale else 'off'
        self.avto_on_off(var)
        self.pop_up(self.board.canvw)
        dir_ = config.get('Dir', 'dirprj')
        self.scan_pui = RS232(self, self.byte_size, dir_)
        self.state_menu((0, (0, 1), 'disabled'), (2, (0, 1, 2), 'disabled'))        # print, pdf
        self.state_sub_menu((2, (0, 1, 2), (0, 1), 'disabled'))

    def state_menu(self, *args) -> None:        # args = ((name_menu, (number_menu, ...), state), ...)
        """Статус меню"""
        for n in args:
            list_menu = self.dropdown[n[0]].get_list_menu()
            if list_menu is not None:
                for i in n[1]:
                    list_menu[i].configure(state=n[2])

        # sub = self.dropdown[2].get_sub_menus()      # menu=Вид
        # if sub:
        #     sb = sub[1].get_list_menu()             # submenu=Профиль
        #     sb[0].configure(state="disabled")       # Вкл.

    def state_sub_menu(self, *args):       # args = ((name_menu, (number_menu, ...), (num_sub_menu, ...), state), ...)
        """Статус субменю"""
        for n in args:
            sub = self.dropdown[n[0]].get_sub_menus()
            if sub:
                for i in n[1]:
                    sb = sub[i].get_list_menu()
                    for j in n[2]:
                        sb[j].configure(state=n[3])

    def create_menu(self) -> None:
        """Создание меню"""
        menu = CTkTitleMenu(self, padx=10, x_offset=50)
        hover_color = ('#6699cc', '#003366')
        button_1 = menu.add_cascade("Файл", hover_color=hover_color)
        button_2 = menu.add_cascade("Пуи", hover_color=hover_color)
        button_3 = menu.add_cascade("Вид", hover_color=hover_color)
        button_4 = menu.add_cascade("Сайт", hover_color=hover_color)
        dropdown1 = CustomDropdownMenu(widget=button_1, width=120)
        self.dropdown.append(dropdown1)
        dropdown1.add_option(option="Просмотр PDF", image=im_dict['pdf'], command=self.view_pdf)
        dropdown1.add_option(option="Печать", image=im_dict['print'], command=self.view_pdf)
        dropdown1.add_separator()
        dropdown1.add_option(option="Выход", image=im_dict['exit'], command=self.on_closing)
        dropdown2 = CustomDropdownMenu(widget=button_2, width=140)
        self.dropdown.append(dropdown2)
        dropdown2.add_option(option="Чтение ПУИ", image=im_dict['pui'], command=self.read_pui)
        dropdown2.add_option(option="Просмотр памяти", image=im_dict['mem'], command=self.view_mem)
        dropdown3 = CustomDropdownMenu(widget=button_3, width=110)
        self.dropdown.append(dropdown3)
        sub_menu1 = dropdown3.add_submenu("Сетка", image=im_dict['grid'])
        sub_menu1.add_option(option="   Вкл.", command=lambda: self.grid_on_off('on'))
        sub_menu1.add_option(option="   Выкл.", command=lambda: self.grid_on_off('off'))
        sub_menu2 = dropdown3.add_submenu("Профиль", image=im_dict['dno'])
        sub_menu2.add_option(option="   Вкл.", command=lambda: self.dno_on_off('on'))
        sub_menu2.add_option(option="   Выкл.", command=lambda: self.dno_on_off('off'))
        sub_menu3 = dropdown3.add_submenu("Масштаб", image=im_dict['im16'])
        sub_menu3.add_option(option="   Авто", command=lambda: self.avto_on_off('on'))
        sub_menu3.add_option(option="   Ручной", command=lambda: self.avto_on_off('off'))
        dropdown3.add_separator()
        sub_menu4 = dropdown3.add_submenu("Тема", image=im_dict['tema'])
        sub_menu4.add_option(option="   Dark", command=lambda: self.change_app_mode('Dark'))
        sub_menu4.add_option(option="   Light", command=lambda: self.change_app_mode('Light'))
        dropdown4 = CustomDropdownMenu(widget=button_4, width=140)
        self.dropdown.append(dropdown4)
        dropdown4.add_option(option="www.navi-dals", image=im_dict['link'], command=self.show_web_page)

    def pop_up(self, frame):
        pp = CTkPopupMenu(frame, width=160)
        pp.configure(
            values=({'text': 'Чтение ПУИ', 'command': self.read_pui, "image": im_dict['pui']},
                    {'text': 'Чтение памяти', 'image': im_dict['mem'], 'command': self.view_mem},
                    None,
                    {'text': 'Сменить тему', 'command': self.change_app_mode, 'image': im_dict['tema']},
                    None,
                    {'text': 'Выход', 'command': self.on_closing, 'image': im_dict['exit']}))

    def open_log_drop(self, event) -> None:
        """Открытие файла перетаскиванием"""
        self.filename = event.data[:]
        if self.filename[0] == '{' and self.filename[-1] == '}':
            self.filename = event.data[1:-1]
        if self.filename:
            self.view_mem(self.filename)

    @staticmethod
    def show_web_page() -> None:
        """На сайт"""
        import webbrowser
        try:
            url = 'http://www.navi-dals.ru'
            webbrowser.open_new_tab(url)
        except webbrowser.Error:
            pass

    def scan_port(self) -> None:
        """Сканирование портов и определение на каком порту подключен ПУИ порт остаётся открыт!"""
        self.scan_pui.scan()
        if self.scan_pui.ok:
            self.stbar.stbar_pui.set(f"ПУИ подключен к {self.scan_pui.ok}")
            self.port = True
            self.toolbar.b[1].configure(state='disabled')
            self.toolbar.b[2].configure(state='normal')
        else:
            # self.stbar.stbar_pui.set("ПУИ не найден!")
            self.port = False
            Box(title="", message="Нет связи с ПУИ!",
                font=font, icon="cancel")
        self.bell()

    def read_pui(self) -> None:
        """Чтение ПУИ и сохранение данных в файл"""
        if self.scan_pui.ok is None:
            self.scan_port()
        if self.port:
            f = self.scan_pui.save_file()
            if f:
                var = self.scan_pui.get_path()[1]
                config.set('Dir', 'dirprj', var)
                # self.stbar.stbar_file.set('Чтение данных из ПУИ')
                self.stbar.stbar_pui.set('Чтение данных из ПУИ')
                self.config(cursor='watch')
                # self.frame_main.configure(cursor="watch")
                self.stbar.progress.pack(side="right", fill="x", padx=(300, 10))
                self.stbar.progress.set(0)
                # self.stbar.progress.start()
                num_str = self.scan_pui.receiv_pui(f)  # read PUI
                self.config(cursor='')
                if num_str is not None:
                    if num_str != self.byte_size:
                        # self.stbar.progress.stop()
                        # self.stbar.stbar_file.set('Сбой в передаче данных')
                        self.stbar.stbar_pui.set('Сбой в передаче данных')
                        Box(title="", message=f'Данные получены не целиком',
                            font=font, icon="warning")
                        self._refr_on()
                    else:
                        # self.stbar.progress.stop()
                        # self.stbar.stbar_file.set('Данные сохранены в файле %s' % f)
                        self.stbar.stbar_pui.set(f'Данные сохранены в файле {f}')
                        Box(title="", message=f'Данные получены успешно',
                            font=font, icon="info")
                        self.toolbar.b[1].configure(state='normal')
                else:
                    # self.stbar.progress.stop()
                    self.stbar.stbar_pui.set('Данные не получены')
                    Box(title="", message=f"Файл {f} не сохранен",
                        font=font, icon="info")
                    self._refr_on()
                self.stbar.progress.pack_forget()
            else:
                self.toolbar.b[1].configure(state='normal')
        else:
            self._refr_on()
            self.stbar.stbar_pui.set("Нет связи с ПУИ!")

    def _refr_on(self) -> None:
        self.port = False
        self.toolbar.b[1].configure(state='normal')

    def view_mem(self, file=None) -> None:
        """Просмотр данных"""
        self.focus_force()
        # self.frame_main.configure(cursor="watch")
        self.configure(cursor="watch")
        data = self.scan_pui.canvas_data(file)                                   # > 4.1 сек
        if data:
            if self.view_data is None:
                self.board.run_(data)
                self.view_data = True
                self.update()
                self.board.canvw.bind("<Configure>", self.board.resize)
                s = self.geometry()  # дёргаю геометрию иначе при разворачивании
                # окна и восстановление не сохраняется предыдущий размер ???
                l_ = s.split("+")[0].split("x")
                l_[0] = str(int(l_[0]) + 1)
                l_[1] = str(int(l_[1]) + 1)
                self.geometry("x".join(l_))
            else:
                self.board.reconfig(data)
            name = self.scan_pui.get_path()[0]  # filename
            if name:  # !!!
                # self.stbar.stbar_file.set(f"{name}")
                self.stbar.stbar_pui.set(f"{name}")
            self.board.resize()
            self.focus_force()
            self.toolbar.bar_right.pack(side='left', padx=40)
            self.toolbar.b[3].configure(state='normal')
            self.toolbar.b[4].configure(state='normal')
            self.state_menu((0, (0, 1), 'normal'), (2, (0, 1, 2), 'normal'))
            self.state_sub_menu((2, (0, 1, 2), (0, 1), 'normal'))
        # self.frame_main.configure(cursor="")
        self.configure(cursor="")

    def print_pdf(self) -> None:
        """Печать экрана"""
        self.get_pdf()

    def view_pdf(self) -> None:
        """Открыть экран в Foxit"""
        self.get_pdf(1)

    def get_pdf(self, verbose=None) -> None:
        """Сразу печатаем (verbose=None) или запускаем Foxit (verbose=1)"""
        if self.view_data:
            Pdf(self, verbose)

    def get_pdf_data(self) -> tuple:
        """Получить данные для pdf"""
        src = self.board.get_src()  # int номер экрана
        data = self.board.get_data()  # данные или None  # canvas_show
        filename = self.scan_pui.get_path()[0]  # имя файла с данными
        w = self.board.W  # текущая ширина холста 768
        scale = self.board.get_scale()  # текущий масштаб
        return w, data, src, scale, filename

    def grid_on_off(self, arg=None):
        """Скрыть показать сетку"""
        if self.view_data:
            self.board.grid__(arg)

    def dno_on_off(self, arg=None):
        """Скрыть показать профиль"""
        if self.view_data:
            self.board.dno(arg)

    def avto_on_off(self, arg=None):
        """Установиь сбросить автомасштаб"""
        if self.view_data:
            self.board.scal_()
        if arg == 'on':
            self.avtoscale = False
        elif arg == 'off':
            self.avtoscale = True
        if not self.avtoscale:
            self.toolbar.br[2].configure(image=im_dict['avto'])
            ToolTip(self.toolbar.br[2], message="Автомасштаб")
        else:
            self.toolbar.br[2].configure(image=im_dict['man'])
            ToolTip(self.toolbar.br[2], message="Ручной масштаб")
        self.avtoscale = not self.avtoscale
        var = '1' if self.avtoscale else '0'
        config.set('Preferens', 'avto', var)

    def next(self):
        """На следующий экран"""
        if self.view_data:
            self.board.next()

    def prev(self):
        """На предыдущий экран"""
        if self.view_data:
            self.board.prev()

    def up(self):
        """Увеличить масштаб"""
        if self.view_data:
            self.board.up()

    def down(self):
        """Уменьшить масштаб"""
        if self.view_data:
            self.board.down()

    def full(self):
        """Полный экран"""
        if self.view_data:
            self.board.full()

    def change_app_mode(self, arg=None) -> None:
        app_mode = ctk.get_appearance_mode()
        if app_mode == 'Dark':
            self._change_appearance_mode('Light')
            self.board.canvw.configure(bg='gray75')
        else:
            self._change_appearance_mode('Dark')
            self.board.canvw.configure(bg='gray65')
        geometry_str = self.geometry()
        tmp = geometry_str.split('x')
        width = tmp[0]
        tmp2 = tmp[-1].split('+')
        height = tmp2[0]
        x = tmp2[1]
        y = str(int(tmp2[2]) + 1)
        self.geometry(f"{width}x{height}+{x}+{y}")      # дергаем окно

    def _change_appearance_mode(self, new_appearance_mode) -> None:
        """Сменить тему"""
        if new_appearance_mode == 'Dark':
            self.s.configure('TSizegrip', background='grey13')
        else:
            self.s.configure('TSizegrip', background='grey90')
        ctk.set_appearance_mode(new_appearance_mode)
        # self.transparent_color = self._apply_appearance_mode(self._fg_color)
        # self.title_top.attributes("-transparentcolor", self.transparent_color)
        config.set('Sys', 'app_mode', new_appearance_mode)
        write_config()

    @staticmethod
    def on_closing(arg=None) -> None:
        """Выход"""
        write_config()
        raise SystemExit()


if __name__ == "__main__":
    app = App()
    app.mainloop()
