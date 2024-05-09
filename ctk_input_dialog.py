
import customtkinter as ctk
import sys


class CTkInputDialog(ctk.CTkToplevel):
    """Диалог"""

    def __init__(self,
                 width: int = 200,
                 height: int = 150,
                 border_width: int = 1,
                 bg_color: str = None,
                 border_color: str = None,
                 fg_color: str | tuple[str, str] = None,
                 text_color: str | tuple[str, str] = None,
                 button_fg_color: str | tuple[str, str] = None,
                 button_hover_color: str | tuple[str, str] = None,
                 button_text_color: str | tuple[str, str] = None,
                 entry_fg_color: str | tuple[str, str] = None,
                 entry_border_color: str | tuple[str, str] = None,
                 entry_text_color: str | tuple[str, str] = None,
                 title: str = "CTkDialog",
                 font: tuple | ctk.CTkFont = None,
                 corner_radius: int = 15,
                 text: str = "CTkDialog"):

        super().__init__(fg_color=fg_color)

        self.width = 150 if width < 150 else width
        self.height = 150 if height < 150 else height

        self._fg_color = ctk.ThemeManager.theme["CTkToplevel"]["fg_color"]\
            if fg_color is None else self._check_color_type(fg_color)
        self._text_color = ctk.ThemeManager.theme["CTkLabel"]["text_color"] \
            if text_color is None else self._check_color_type(button_hover_color)
        self._button_fg_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"] \
            if button_fg_color is None else self._check_color_type(button_fg_color)
        self._button_hover_color = ctk.ThemeManager.theme["CTkButton"]["hover_color"]\
            if button_hover_color is None else self._check_color_type(button_hover_color)
        self._button_text_color = ctk.ThemeManager.theme["CTkButton"]["text_color"]\
            if button_text_color is None else self._check_color_type(button_text_color)
        self._entry_fg_color = ctk.ThemeManager.theme["CTkEntry"]["fg_color"] \
            if entry_fg_color is None else self._check_color_type(entry_fg_color)
        self._entry_border_color = ctk.ThemeManager.theme["CTkEntry"]["border_color"] \
            if entry_border_color is None else self._check_color_type(entry_border_color)
        self._entry_text_color = ctk.ThemeManager.theme["CTkEntry"]["text_color"]\
            if entry_text_color is None else self._check_color_type(entry_text_color)

        self._user_input: str | None = None
        self._running: bool = False
        self._title = title
        self._text = text
        self._font = font
        self.round_corners = corner_radius if corner_radius <= 30 else 30

        self.title(self._title)
        self.lift()  # lift window on top
        self.attributes("-topmost", True)  # stay on top
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        # create widgets with slight delay, to avoid white flickering of background
        self.after(10, self._create_widgets)
        self.resizable(False, False)
        self.grab_set()  # make other windows not clickable

        self.validate_cmd = (self.register(self.is_okay), '%P')

        if sys.platform.startswith("win"):
            self.transparent_color = self._apply_appearance_mode(self.cget("fg_color"))
            self.attributes("-transparentcolor", self.transparent_color)
            # default_cancel_button = "cross"
        elif sys.platform.startswith("darwin"):
            self.transparent_color = 'systemTransparent'
            self.attributes("-transparent", True)
            # default_cancel_button = "circle"
        else:
            self.transparent_color = '#000001'
            # corner_radius = 0
            # default_cancel_button = "cross"

        if bg_color is None:
            self.bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        else:
            self.bg_color = bg_color

        if fg_color is None:
            self.fg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"])
        else:
            self.fg_color = fg_color

        if border_color is None:
            self.border_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["border_color"])
        else:
            self.border_color = border_color

        self.border_width = border_width if border_width < 6 else 5
        # self.button_border_width = button_border_width if button_border_width < 6 else 5

        self.frame_top = ctk.CTkFrame(self, corner_radius=self.round_corners, width=self.width,
                                      border_width=self.border_width, bg_color=self.transparent_color,
                                      fg_color=self.bg_color, border_color=self.border_color)
        self.frame_top.grid(sticky="news")
        self.frame_top.grid_rowconfigure(1, weight=1)
        # self.frame_top.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.bind("<B1-Motion>", self.move_window)
        self.frame_top.bind("<ButtonPress-1>", self.old_xy_set)

    def _create_widgets(self):
        self.grid_columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self._label = ctk.CTkLabel(master=self.frame_top,
                                   width=200,
                                   wraplength=300,
                                   fg_color="transparent",
                                   text_color=self._text_color,
                                   text=self._text,
                                   font=self._font)
        self._label.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 10), sticky="ew")

        self._entry = ctk.CTkEntry(master=self.frame_top,
                                   width=130,
                                   fg_color=self._entry_fg_color,
                                   border_color=self._entry_border_color,
                                   text_color=self._entry_text_color,
                                   font=self._font,
                                   validate='key',
                                   validatecommand=self.validate_cmd)
        self._entry.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

        self._ok_button = ctk.CTkButton(master=self.frame_top,
                                        width=100,
                                        border_width=0,
                                        fg_color=self._button_fg_color,
                                        hover_color=self._button_hover_color,
                                        text_color=self._button_text_color,
                                        text='Ok',
                                        font=self._font,
                                        command=self._ok_event)
        self._ok_button.grid(row=2, column=0, columnspan=1, padx=(20, 10), pady=(0, 10), sticky="ew")

        self._cancel_button = ctk.CTkButton(master=self.frame_top,
                                            width=100,
                                            border_width=0,
                                            fg_color=self._button_fg_color,
                                            hover_color=self._button_hover_color,
                                            text_color=self._button_text_color,
                                            text='Cancel',
                                            font=self._font,
                                            command=self._cancel_event)
        self._cancel_button.grid(row=2, column=1, columnspan=1, padx=(10, 20), pady=(0, 10), sticky="ew")

        self.after(150, lambda: self._entry.focus())  # set focus to entry with slight delay, otherwise it won't work
        self._entry.bind("<Return>", self._ok_event)

    @staticmethod
    def is_okay(par: str) -> bool:
        """Если возвращает False, то значение не изменить"""
        try:
            par = int(par)
        except (ValueError, TypeError):
            return False
        if par <= 0:
            return False
        return True

    def _ok_event(self, event=None):
        self._user_input = self._entry.get()
        self.grab_release()
        self.destroy()

    def _on_closing(self):
        self.grab_release()
        self.destroy()

    def _cancel_event(self):
        self.grab_release()
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return self._user_input

    def old_xy_set(self, event) -> None:
        self.old_x = event.x
        self.old_y = event.y

    def move_window(self, event) -> None:
        self.y = event.y_root - self.old_y
        self.x = event.x_root - self.old_x
        self.geometry(f'+{self.x}+{self.y}')
