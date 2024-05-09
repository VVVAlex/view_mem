import math
import tkinter as tk
import customtkinter as ctk
from common import config, family, font_size_14
from ctk_input_dialog import CTkInputDialog

color1 = color2 = "blue"
color3 = color4 = "brown"
color_f = "#282828"
color_p = "#f59400"
color_t = "black"
# color_d = "darkgreen"

offset_x = 15
offset_y = 12
offset_d = 43

font = (family, font_size_14)


class Fild(ctk.CTkFrame):
    """Класс холста просмотра + информ.лабель"""

    def __init__(self, root, **kwargs):
        self.root = root
        super().__init__(root, **kwargs)
        self.mult = (1, 2, 5, 10, 20, 40, 100, 200, 300, 400)
        self.step = (0, 5, 10, 15, 20, 25, 30, 35)
        self.W = 1000
        self.H = 600
        self.color__ = "gray85"             #
        self.m_top = 20  # 35 for notebook 7
        self.m_right = 65  # 55
        self.m_bottom = 35
        self.m_left = 25  # margin4
        # self.font = ('tahoma', '12', 'bold')        # Helvetica bold italic
        # self.font = ctk.CTkFont(family=f"{family}", size=font_size, weight='bold')
        self.n = 0
        self.n__ = 8
        self.scale = 0  # scale 0,1,2,3,4,5,6,7 +4000, 6000
        self.screen = 1  # текущий экран
        self.marker_on = 0
        self.fullscreen = 0
        self.id = None
        self.start = None
        self.k = self.mult[self.scale]
        self.dno_ = config.getboolean('Preferens', 'dno')
        self.grid_ = config.getboolean('Preferens', 'grid')
        self.day = ''
        self.data = None
        self.n_screen = 0
        self.data_full = None
        self.frame_canv = ctk.CTkFrame(self)
        w = self.W + self.m_right + self.m_left
        self.canvw = tk.Canvas(
            self.frame_canv,
            width=w,
            height=self.H + self.m_top + self.m_bottom,
            bg="gray65",
            relief="ridge",
            bd=0,
        )
        self.canvw.config(highlightthickness=0, takefocus=1)

    def run_(self, data: list = None) -> None:
        """Показ данных"""
        self.data_full = data  # all data
        self.canvw.pack(fill="both", expand=True)
        self.frame_canv.pack(fill="both", expand=True)
        if self.data_full:
            self.n_screen = self.get_maxscreen()  # число экранов
            self.data = self.data_full[:self.W]
            self._calk_scale()
            self.root.head.set_scr_num(self.screen)
            # self.k = self.mult[self.scale]
            # self.dno_ = False  # не подсвечивать рельеф при старте
            self.create_fild(self.canvw)
            self.text_axis(self.canvw)
            if self.grid_:
                self.set_grid()
        self.bind_()

    def create_fild(self, canv: tk.Canvas) -> None:
        """Рисуем поле с осями"""
        w, h, m_top, m_right, m_bottom, m_left = (
            self.W,
            self.H,
            self.m_top,
            self.m_right,
            self.m_bottom,
            self.m_left,
        )
        line = canv.create_line
        canv.config(width=w + m_right + m_left, height=h + m_top + m_bottom)
        canv.create_rectangle(
            m_left, m_top, m_left + w, m_top + h, fill=color_f, tags="fild"
        )
        line(
            m_left - 1,
            m_top,
            m_left - 1,  # axis
            m_top + h,
            width=2,
            fill=color4,
            tags="fild",
        )  # 4 left
        line(
            m_left + w + 2,
            m_top,
            m_left + w + 2,
            m_top + h,
            width=2,
            fill=color2,
            tags="fild",
        )  # 2 right
        line(
            m_left - 1,
            m_top,
            m_left + w + 1,  # 1 top
            m_top,
            width=2,
            fill=color1,
            tags="fild",
        )
        line(
            m_left - 2,
            m_top + h,  # 3 bottom
            m_left + w + 2,
            m_top + h,
            width=2,
            fill=color3,
            tags="fild",
        )
        for N in range(8):
            t = 10 if N % 2 == 0 else 7  # len tick short ant long
            line(
                m_left + w + 2,
                m_top + N * h // 8,
                m_left + w + 2 + t,
                m_top + N * h // 8,  # tick_Y
                width=2,
                fill=color1,
                tags="fild",
            )
            line(
                m_left + N * w // 8 - 2,
                m_top + h,
                m_left + N * w // 8 - 2,
                m_top + h + t,  # tick_X
                width=2,
                fill=color3,
                tags="fild",
            )

    def set_grid(self) -> None:
        """Показать сетку"""
        self.grid_ = True  # grid on
        for N in range(8):
            self.canvw.create_line(
                self.m_left,
                self.m_top + N * self.H // 8,
                self.m_left + self.W,
                self.m_top + N * self.H // 8,  # grid_X
                width=1,
                dash=(3, 5),
                fill="gray55",
                tags="grid",
            )
            self.canvw.create_line(
                self.m_left + N * self.W // 8 - 2,
                self.m_top + self.H,
                self.m_left + N * self.W // 8 - 2,
                self.m_top,  # grid_Y
                width=1,
                dash=(3, 5),
                fill="gray55",
                tags="grid",
            )

    def clr_grid(self) -> None:
        """Убрать сетку"""
        self.grid_ = False  # grid off
        self.canvw.delete("grid")

    def text_axis(self, canv: tk.Canvas) -> None:
        """Наносим на оси время и дату по Y всё по X только в начале"""
        w, h, m_top, m_left = self.W, self.H, self.m_top, self.m_left
        text = canv.create_text
        for i in range(5):
            txt_y = self.step[i] * self.k
            text(
                m_left + w + offset_x,
                m_top + i * h // 4,
                text=f"{txt_y:2d}",  # text_Y
                anchor="w",
                font=font,
                fill=color_t,        # "darkblue",
                tags="text",
            )
        txt_x = self.data[0].time[:5]
        self.day = txt_xd = self.data[0].day
        if txt_x and txt_xd:
            text(
                m_left + w - 16,
                m_top + h + offset_y,
                text=f"{txt_x}/{txt_xd}",  # text_X_time0
                anchor="n",
                font=font,
                fill="black",
                tags="text",
            )

    def set_data(self, canv: tk.Canvas) -> None:
        """Выводим данные и надписи на осях и метки"""
        w, h, m_top, m_left = self.W, self.H, self.m_top, self.m_left
        line = canv.create_line
        for j in range(w):
            if j < len(self.data):
                y = self.data[j].glub / self.k * h / 200
                if y < h and y != 0:
                    line(
                        m_left + w - j,
                        m_top + y,
                        m_left + w - j,
                        h + m_top - 2,
                        fill=color_f,
                        tags="dno",
                    )  # дно рисуем раньше точек (иначе затрём нижние цели)
                if y < h and y != 0:
                    line(
                        m_left + w - j,
                        m_top + y,  # point one
                        m_left + w - j,
                        m_top + y + 2,
                        fill=color_p,
                        width=1,
                        tags="point",
                    )

                if j == w // 4 - 1:
                    self.create_tex(j, 3, 4)
                if j == w // 2 - 1:
                    self.create_tex(j, 1, 2)
                if j == w * 3 // 4 - 1:
                    self.create_tex(j, 1, 4)
                if j == w - 1:
                    self.create_tex(j, 0, 1)

    def create_tex(self, j, numerator: int, denominator: int) -> None:
        w, h, m_top, m_left = self.W, self.H, self.m_top, self.m_left
        k = w * numerator // denominator
        txt_x = self.data[j].time[:5]        # Вемя 11:23
        text = self.canvw.create_text
        text(
            m_left + k,
            m_top + h + offset_y,
            text=f"{txt_x}",  # text_X_time_
            anchor="n",
            font=font,
            fill=color_t,
            tags="text",
        )
        if self.day != self.data[j].day:
            txt_xd = self.data[j].day           # Дата 30.12
            text(
                m_left + k + offset_d + 10,
                m_top + h + offset_y,
                text=f"/{txt_xd}",  # text_X_data1
                anchor="n",
                font=font,
                fill=color_f,
                tags="text",
            )
            self.day = txt_xd

    def dno(self, arg=None) -> None:
        """Cкрыть показать профиль"""
        if arg is None:
            color_dno = color_f if self.dno_ else "#505050"
            self.dno_ = not self.dno_
        elif arg == 'on':
            color_dno = "#505050"
            self.dno_ = True
        elif arg == 'off':
            color_dno = color_f
            self.dno_ = False
        else:
            return
        self.canvw.itemconfigure("dno", fill=color_dno)
        if self.grid_:
            self.set_grid()
        var = '1' if self.dno_ else '0'
        config.set('Preferens', 'dno', var)

    def grid__(self, arg=None) -> None:
        """Cкрыть или показать сетку"""
        if arg is None:
            self.clr_grid() if self.grid_ else self.set_grid()
        elif arg == 'on':
            self.set_grid()
        elif arg == 'off':
            self.clr_grid()
        var = '1' if self.grid_ else '0'
        config.set('Preferens', 'grid', var)

    def next(self, arg=None) -> None:
        """На следующий экран"""
        if self.screen < self.n_screen:
            self.screen += 1
            self.datascreen()

    def prev(self, arg=None) -> None:
        """На предыдущий экран"""
        if self.screen > 1:
            self.screen -= 1
            self.datascreen()

    def up(self, arg=None) -> None:
        """Увеличить масштаб"""
        if self.scale < self.n__:  # 9 for 10000м
            self.scale += 1
            self.update_data()

    def down(self, arg=None) -> None:
        """Уменьшить масштаб"""
        if self.scale > 0:
            self.scale -= 1
            self.update_data()

    def full(self, arg=None) -> None:
        """Полный экран"""
        if self.root.view_data:
            self.enter_() if self.fullscreen else self._data_fullscreen()

    def next_one(self, event) -> None:
        """Переместить маркер влево на 1px"""
        if self.start is not None:
            if self.W + self.m_left + 1 > self.start.x > self.m_left:
                self.canvw.delete("marker")
                self.start.x -= 1
                self._marker(self.canvw, self.start)

    def prev_one(self, event) -> None:
        """Переместить маркер вправо на 1px"""
        if self.start is not None:
            if self.W + self.m_left > self.start.x > self.m_left - 1:
                self.canvw.delete("marker")
                self.start.x += 1
                self._marker(self.canvw, self.start)

    def go_screen(self, arg=None):
        """Переход на заданый экран"""
        dialog = CTkInputDialog(text="Введите номер экрана:", title="",
                                font=("Roboto Medium", -14))
        dialog.overrideredirect(1)
        x = 150 + self.winfo_rootx()
        y = 100 + self.winfo_rooty()
        dialog.geometry(f"+{x}+{y}")
        rez = dialog.get_input()
        if rez:
            scr = int(rez)
            if scr > self.n_screen:
                scr = self.n_screen
            self.screen = scr
            self.datascreen()

    def bind_(self, arg=None) -> None:
        self.root.bind("<Control-g>", self.go_screen)
        self.canvw.bind("<ButtonPress-1>", self._on_marker)
        self.canvw.bind("<ButtonRelease-1>", self._release)
        self.canvw.bind("<B1-Motion>", self._move_marker)
        self.canvw.bind("<Double-1>", self.enter_)
        self.canvw.bind_all("<Escape>", self._clear_marker)
        self.bind_2()

    def bind_2(self, arg=None) -> None:
        self.canvw.bind_all("<Home>", self._home)
        self.canvw.bind_all("<End>", self._end)
        self.canvw.bind_all("<Up>", self.up)
        self.canvw.bind_all("<Down>", self.down)
        self.canvw.bind_all("<Left>", self.next)
        self.canvw.bind_all("<Right>", self.prev)
        self.canvw.bind_all("<Control-Left>", self.next_one)
        self.canvw.bind_all("<Control-Right>", self.prev_one)

    def unbind_(self, arg=None) -> None:
        self.canvw.unbind("<ButtonPress-1>")
        self.canvw.unbind("<ButtonRelease-1>")
        self.canvw.unbind("<B1-Motion>")
        self.canvw.unbind("<Double-1>")
        self.canvw.unbind("<Double-2>")
        self.canvw.unbind_all("<Escape>")
        self.unbind_2()

    def unbind_2(self, arg=None) -> None:
        self.canvw.unbind_all("<Home>")
        self.canvw.unbind_all("<End>")
        self.canvw.unbind_all("<Up>")
        self.canvw.unbind_all("<Down>")
        self.canvw.unbind_all("<Left>")
        self.canvw.unbind_all("<Right>")
        self.canvw.unbind_all("<Control-Left>")
        self.canvw.unbind_all("<Control-Right>")

    def enter_(self, arg=None):
        """Обработка поля ввода номера экрана"""
        try:
            self.screen = int(self.root.head.get_scr_num())
            if self.screen > self.n_screen:
                self.screen = self.n_screen
            if self.screen < 1:
                self.screen = 1
            self.canvw.focus_set()
            self.datascreen()
        except ValueError:
            self.root.head.set_scr_num('')

    def resize(self, event=None) -> None:
        """Изменение размера холста при измкнении размера окна"""
        if self.canvw.winfo_geometry() != "1x1+0+0":
            canvw, canvh = self.canvw.winfo_width(), self.canvw.winfo_height()
            self.W, self.H = (
                canvw - self.m_left - self.m_right,
                canvh - self.m_bottom - self.m_top,
            )
        self.reconfig()

    def _end(self, event=None) -> None:
        """На последний экран"""
        self.screen = self.n_screen
        self.datascreen()

    def _home(self, event=None) -> None:
        """На первый экран"""
        self.screen = 1
        self.datascreen()

    def _next(self, event=None) -> None:
        """На следующий экран"""
        if self.screen < self.n_screen:
            self.screen += 1
            self.datascreen()

    def _prev(self, event=None) -> None:
        """На предыдущий экран"""
        if self.screen > 1:
            self.screen -= 1
            self.datascreen()

    def _data_fullscreen(self, event=None) -> None:
        """Полный экран"""
        k = self.n_screen
        data = self.data_full[0:self.W * k:k]
        self.fullscreen = 1
        if data:
            self.reload_fild(data)
        if self.start:  # not None (=event) когда есть маркер
            self.canvw.delete("marker")

    def update_scr(self) -> None:
        """Обновить номер экрана при полном экране"""
        x = self.start.x  # координата маркера
        scr_w = int(self.n_screen * (x - 20) / self.W)
        scr = self.n_screen - scr_w
        self.screen = scr
        self.root.head.set_scr_num(scr)

    def datascreen(self) -> None:
        """Новый срез данных"""
        self.fullscreen = 0
        if self.screen > self.n_screen:
            self.screen = self.n_screen
        data = self.data_full[self.W * (self.screen - 1):self.W * self.screen]
        if data:
            self.reload_fild(data)

    def reload_fild(self, data: list) -> None:
        """Подготовка для перерисовки поля"""
        self.data = data
        self.root.head.set_scr_num(self.screen)
        if self.root.avtoscale:
            self._calk_scale()
        self.update_data()

    def update_data(self) -> None:
        """Перерисовать поле и оси"""
        for v in (
            "text",
            "point",
            "dno",
            "marker",
            "grid",
        ):
            try:
                self.canvw.delete(v)
            except tk.TclError:
                pass
        self.k = self.mult[self.scale]
        self.text_axis(self.canvw)
        self.set_data(self.canvw)
        if self.dno_:
            self.canvw.itemconfigure("dno", fill="#505050")
        if self.grid_:
            self.set_grid()
        if self.marker_on:
            self._marker(self.canvw)

    def reconfig(self, data: list = None) -> None:
        """Перерисовка всего холста при изменении его размера"""
        if data:
            self.data_full = data
        self.canvw.delete("fild")
        self.create_fild(self.canvw)
        self.canvw.delete("marker")  # иначе будет на другой позиции
        self.get_maxscreen()
        self.datascreen()  # вместо update_data() иначе не полностью перерисовываются данные

    def delete_data(self) -> None:
        """Очищаем поле"""
        for v in (
            "text",
            "point",
            "dno",
            "marker",
            "grid",
        ):
            try:
                self.canvw.delete(v)
            except tk.TclError:
                pass

    def index_(self, event):
        """Позиция в данных"""
        index = (self.W + self.m_left) - event.x if event else (self.W + self.m_left) - self.start.x
        if index < len(self.data):  # self.W
            return index

    def info(self, event):
        """Инициализация переменных по данным"""
        index = self.index_(event)
        if index is not None:
            glub = self.data[index].glub / 10.      # glubina
            t = ' '.join([self.data[index].day, self.data[index].time])  # data + time
            schir = self.data[index].shir  # schirota
            if schir == '00.000.00':
                schir = ''
            dolg = self.data[index].dolg  # dolgota
            if dolg == '000.00.000':
                dolg = ''
            gl = glub if glub else ''
            color = self.root.head.color
            for i in self.root.head.lab:
                i.configure(text_color=color)
            self.root.head.set_(gl, schir, dolg, t)

    def _marker(self, canv, event=None) -> None:
        """Рисуем маркер"""
        color_m = "green"
        color_md = "magenta"  # red
        x = event.x if event else self.start.x
        y = self.m_top
        h = self.H
        line = canv.create_line
        line(x, y, x, y + h, width=1, fill=color_m, tags="marker")
        line(x + 1, y, x + 1, y + 5, width=1, fill=color_md, tags="marker")
        line(x + 2, y, x + 2, y + 3, width=1, fill=color_md, tags="marker")
        line(x - 1, y, x - 1, y + 5, width=1, fill=color_md, tags="marker")
        line(x - 2, y, x - 2, y + 3, width=1, fill=color_md, tags="marker")
        line(x + 1, y + h, x + 1, y + h - 5, width=1, fill=color_m, tags="marker")
        line(x + 2, y + h, x + 2, y + h - 3, width=1, fill=color_m, tags="marker")
        line(x - 1, y + h, x - 1, y + h - 5, width=1, fill=color_m, tags="marker")
        line(x - 2, y + h, x - 2, y + h - 3, width=1, fill=color_m, tags="marker")
        index = self.index_(event)  # light marker
        if index is not None:
            try:
                dat = self.data[index].glub / self.k * h / 200  # [1]
                if dat > h - 5:
                    dat = h - 5
                line(x, y + 5, x, y + dat, fill=color_md, tags="marker")
            except IndexError:
                pass
        self.info(event)

    def update_screen(self, event) -> None:
        """Перейти на следующий или предыдущий экран"""
        if event.x <= self.m_left and self.m_top + self.H > event.y > self.m_top:
            self._next()
        if (
            event.x >= self.W + self.m_left
            and self.m_top + self.H > event.y > self.m_top
        ):
            self._prev()

    def a_cancel(self) -> None:
        """Отвязать пролистывание экранов после repid()"""
        if self.id:
            self.canvw.after_cancel(self.id)
            self.id = None

    def _release(self, event=None):  # отпускание кнопки 1 мыши
        self.canvw.configure(cursor="")
        self.a_cancel()

    def notfild(self) -> None:
        """Пролистываем экраны когда курсор не в поле"""
        if self.fullscreen == 0:
            self.marker_on = 0
            if self.id is None:
                self.repid()

    def _on_marker(self, event) -> None:
        """Показать маркер"""
        self.canvw.delete("marker")
        self.start = event  # запомнить позицию маркера
        if (
            self.W + self.m_left + 1 > event.x > self.m_left - 1
            and self.m_top + self.H > event.y > self.m_top
        ):
            self.canvw.configure(cursor="cross")  # cross, sb_h_double_arrow
            self.marker_on = 1
            self._marker(self.canvw, event)  # нарисовать маркер
            self.a_cancel()
            if self.fullscreen:
                self.update_scr()
        else:
            self.notfild()

    def _move_marker(self, event) -> None:
        """Переместить маркер"""
        if (
            self.W + self.m_left + 1 > event.x > self.m_left - 1
            and self.m_top + self.H > event.y > self.m_top
        ):
            self.canvw.delete("marker")
            self.marker_on = 1
            self.start = event  # запомнить позицию маркера
            self._marker(self.canvw, event)  # нарисовать маркер
            self.a_cancel()
            if self.fullscreen:
                self.update_scr()
        else:
            self.notfild()

    def _clear_marker(self, event=None) -> None:
        """Погасить маркер"""
        self.canvw.delete("marker")
        self.marker_on = 0
        # self.clr_var()

    def repid(self) -> None:
        """Если надо, то сменить экран через 0.6 сек на след./предыд."""
        self.update_screen(self.start)
        self.id = self.canvw.after(
            800, self.repid
        )  # возвращает целый id для after_cancel

    def _calk_scale(self) -> None:
        """Вычислить масштаб"""
        mx = [i.glub for i in self.data]
        m = max(mx) / 10
        for i, j in (
            (1, 0),
            (2, 1),
            (5, 2),
            (10, 3),
            (20, 4),
            (40, 5),
            (100, 6),
            (200, 7),
            (300, 8),
        ):
            if m / i < 20:
                self.scale = j
                break

    def scal_(self, event=None) -> None:
        """Изменить масштаб экрана"""
        self._calk_scale()
        self.update_data()

    def get_scale(self) -> int:
        """Вернуть масштаб 0-7"""
        return self.scale

    def get_src(self) -> int:
        """Вернуть номер экрана"""
        return self.screen

    def get_data(self) -> list:
        """Вернуть текущие данные"""
        return self.data

    def get_maxscreen(self) -> int:
        """Вернуть число экранов"""
        n_screen = int(math.ceil(len(self.data_full) * 1.0 / self.W))
        self.n_screen = n_screen
        return n_screen
