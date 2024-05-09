
import time
import sys
import customtkinter
from tkinter import Toplevel, Frame


class CTkToolTip(Toplevel):
    """Создание всплывающих подсказок"""

    def __init__(
            self,
            widget: any = None,
            message: str = None,
            delay: float = 0.3,
            follow: bool = True,
            x_offset: int = +20,
            y_offset: int = +20,
            bg_color: str = None,
            corner_radius: int = 10,
            border_width: int = 2,
            border_color: str = None,
            alpha: float = 0.95,
            padding: tuple = (10, 0),
            **message_kwargs):

        super().__init__()

        self.widget = widget

        self.withdraw()

        # Disable ToolTip's title bar
        self.overrideredirect(True)

        if sys.platform.startswith("win"):
            self.transparent_color = self.widget._apply_appearance_mode(
                customtkinter.ThemeManager.theme["CTkToplevel"]["fg_color"])
            self.attributes("-transparentcolor", self.transparent_color)
            self.transient()
        elif sys.platform.startswith("darwin"):
            self.transparent_color = 'systemTransparent'
            self.attributes("-transparent", True)
            self.transient(self.master)
        else:
            self.transparent_color = '#000001'
            corner_radius = 0
            self.transient()

        self.resizable(width=True, height=True)

        # Make the background transparent
        self.config(background=self.transparent_color)

        # StringVar instance for msg string
        self.messageVar = customtkinter.StringVar()
        self.message = message
        self.messageVar.set(self.message)

        self.delay = delay
        self.follow = follow
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.corner_radius = corner_radius
        self.alpha = alpha
        self.border_width = border_width
        self.padding = padding
        self.bg_color = customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"] if bg_color is None else bg_color
        self.border_color = border_color
        self.disable = False

        # visibility status of the ToolTip inside|outside|visible
        self.status = "outside"
        self.last_moved = 0
        self.attributes('-alpha', self.alpha)

        if sys.platform.startswith("win"):
            if self.widget._apply_appearance_mode(self.bg_color) == self.transparent_color:
                self.transparent_color = "#000001"
                self.config(background=self.transparent_color)
                self.attributes("-transparentcolor", self.transparent_color)

        # Add the message widget inside the tooltip
        self.transparent_frame = Frame(self, bg=self.transparent_color)
        self.transparent_frame.pack(padx=0, pady=0, fill="both", expand=True)

        self.frame = customtkinter.CTkFrame(self.transparent_frame, bg_color=self.transparent_color,
                                            corner_radius=self.corner_radius,
                                            border_width=self.border_width, fg_color=self.bg_color,
                                            border_color=self.border_color)
        self.frame.pack(padx=0, pady=0, fill="both", expand=True)

        self.message_label = customtkinter.CTkLabel(self.frame, textvariable=self.messageVar, **message_kwargs)
        self.message_label.pack(fill="both", padx=self.padding[0] + self.border_width,
                                pady=self.padding[1] + self.border_width, expand=True)
        # print(self.widget.winfo_name())
        # if self.widget.winfo_name() != "tk":
        #     if self.frame.cget("fg_color") == self.widget.cget("bg_color"):
        #         if not bg_color:
        #             self._top_fg_color = self.frame._apply_appearance_mode(
        #                 customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"])
        #             if self._top_fg_color != self.transparent_color:
        #                 self.frame.configure(fg_color=self._top_fg_color)

        self.widget.bind("<Enter>", self.on_enter, add="+")
        self.widget.bind("<Leave>", self.on_leave, add="+")
        self.widget.bind("<Motion>", self.on_enter, add="+")
        self.widget.bind("<B1-Motion>", self.on_enter, add="+")
        self.widget.bind("<Destroy>", lambda _: self.hide(), add="+")

    def show(self) -> None:
        """Разрешить виджет"""
        self.disable = False

    def on_enter(self, event) -> None:
        """Обрабатывает движение внутри виджета, включая ввод и перемещение"""
        if self.disable:
            return
        self.last_moved = time.time()

        # Установите статус inside в самый первый раз
        if self.status == "outside":
            self.status = "inside"

        # Если флажок follow не установлен, при движении внутри виджета всплывающая подсказка исчезнет
        if not self.follow:
            self.status = "inside"
            self.withdraw()

        # Рассчитывает доступное пространство в правой части виджета относительно экрана
        root_width = self.winfo_screenwidth()
        widget_x = event.x_root
        space_on_right = root_width - widget_x

        # Рассчитывает ширину текста всплывающей подсказки на основе длины строки сообщения
        text_width = self.message_label.winfo_reqwidth()

        # Рассчитывает смещение, основываясь на доступном пространстве и ширине текста,
        # чтобы избежать перехода за пределы экрана с правой стороны
        offset_x = self.x_offset
        if space_on_right < text_width + 20:  # Adjust the threshold as needed
            offset_x = -text_width - 20  # Negative offset when space is limited on the right side

        # Смещает всплывающую подсказку, используя координаты события в качестве отправной точки
        self.geometry(f"+{event.x_root + offset_x}+{event.y_root + self.y_offset}")

        self.after(int(self.delay * 1000), self._show)

    def on_leave(self, event=None) -> None:
        """Временно скрывает всплывающую подсказку"""

        if self.disable: return
        self.status = "outside"
        self.withdraw()

    def _show(self) -> None:
        """Отображает всплывающую подсказку"""

        if not self.widget.winfo_exists():
            self.hide()
            self.destroy()

        if self.status == "inside" and time.time() - self.last_moved >= self.delay:
            self.status = "visible"
            self.deiconify()

    def hide(self) -> None:
        """Отключить отображение виджета"""
        if not self.winfo_exists():
            return
        self.withdraw()
        self.disable = True

    def is_disabled(self) -> None:
        """Возвращает состояние окна"""
        return self.disable

    def get(self) -> None:
        """Возвращает текст во всплывающей подсказке"""
        return self.messageVar.get()

    def configure(self, message: str = None, delay: float = None, bg_color: str = None, **kwargs) -> None:
        """Конфигурация виджета"""
        if delay:
            self.delay = delay
        if bg_color:
            self.frame.configure(fg_color=bg_color)
        self.messageVar.set(message)
        self.message_label.configure(**kwargs)
