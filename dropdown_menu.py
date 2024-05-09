
import customtkinter
from functools import partial
import tkinter as tk
from typing import Callable


class _CDMOptionButton(customtkinter.CTkButton):
    def set_parent_menu(self, menu: "CustomDropdownMenu"):
        self.parent_menu = menu


class _CDMSubmenuButton(_CDMOptionButton):
    def set_submenu(self, submenu: "CustomDropdownMenu"):
        self.submenu = submenu


class CustomDropdownMenu(customtkinter.CTkFrame):
    
    def __init__(self, 
                 widget: customtkinter.CTkBaseClass | _CDMSubmenuButton,
                 master: any = None,
                 border_width: int = 1,
                 width: int = 270,
                 height: int = 25,
                 bg_color: str | tuple[str, str] = None,
                 corner_radius: int = 5,
                 border_color: str | tuple[str, str] = None,        # "grey50",
                 separator_color: str | tuple[str, str] = ("grey80", "grey20"),
                 text_color: str | tuple[str, str] = ("black", "white"),
                 fg_color: str | tuple[str, str] = "transparent",
                 hover_color: str | tuple[str, str] = ("grey75", "grey25"),         # None, синий
                 font: customtkinter.CTkFont = ("helvetica", 12),
                 padx: int = 3,
                 pady: int = 3,
                 cursor: str = "hand2",
                 **kwargs):
        
        if widget.master.winfo_name().startswith("!ctktitlemenu"):
            widget.master.master.bind("<ButtonPress>", self._check_if_mouse_left, add="+")
            widget.master.master.bind("<Button-1>", self._check_if_mouse_left, add="+")
            master = widget.master if master is None else master
            widget.master.menu.append(self)
            
        elif widget.master.winfo_name().startswith("!ctkmenubar"):
            widget.winfo_toplevel().bind("<ButtonPress>", self._check_if_mouse_left, add="+")
            widget.winfo_toplevel().bind("<Button-1>", self._check_if_mouse_left, add="+")
            master = widget.master.master if master is None else master
            widget.master.menu.append(self)
        else:
            widget.winfo_toplevel().bind("<ButtonPress>", self._check_if_mouse_left, add="+")
            widget.winfo_toplevel().bind("<Button-1>", self._check_if_mouse_left, add="+")
            master = widget.master if master is None else master
            
        super().__init__(
            master=master,
            border_width=border_width,
            fg_color=bg_color,
            border_color=border_color,
            corner_radius=corner_radius,
            **kwargs)

        self.border_color = border_color
        self.border_width = border_width
        self.bg_color = bg_color
        self.corner_radius = corner_radius
        self.menu_seed_object = widget
        self.master = master
        self.menu_seed_object.configure(command=self.toggle_show)
        self.fg_color = fg_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.font = font
        self.height = height
        self.width = width
        self.padx = padx
        self.pady = pady
        self.cursor = cursor
        self.hovered = False

        self.separator_color = separator_color
        self._options_list: list[_CDMOptionButton | _CDMSubmenuButton] = []
        
    def select_option(self, command) -> None:
        self._hide_all_menus()
        if command:
            command()
        
    def dummy(self) -> None:
        pass
    
    def add_option(self, option: str, image=None, command: Callable = dummy, **kwargs) -> None:
        # fg_color = kwargs.pop('fg_color', self.fg_color)
        # hover_color = kwargs.pop('hover_color', self.hover_color)
        text_color = kwargs.pop('text_color', self.text_color)
        font_ = kwargs.pop('font', self.font)
        option_button = _CDMOptionButton(
            self,
            width=self.width,
            height=self.height,
            text=option,
            image=image,
            compound='left',
            anchor="w",
            # text_color=self.text_color,
            # hover_color=hover_color,
            # fg_color=fg_color,
            text_color=text_color,
            font=font_,
            command=partial(self.select_option, command),
            **kwargs)
        option_button.configure(cursor=self.cursor)
        # print(f'cget {option_button.cget('font')}')
        
        option_button.set_parent_menu(self)
        self._options_list.append(option_button)
        self._configure_button(option_button)

        option_button.pack(
            side="top",
            fill="both", 
            expand=True,
            padx=3+(self.corner_radius/5),
            pady=3+(self.corner_radius/5))
    
    def add_submenu(self, submenu_name: str, **kwargs) -> "CustomDropdownMenu":
        submenu_button_seed = _CDMSubmenuButton(self, text=submenu_name, anchor="w",
                                                text_color=self.text_color,
                                                width=self.width, height=self.height, **kwargs)
        submenu_button_seed.set_parent_menu(self)
        self._options_list.append(submenu_button_seed)
        self._configure_button(submenu_button_seed)

        submenu = CustomDropdownMenu(
            master=self.master,
            height=self.height,
            width=self.width,
            widget=submenu_button_seed,
            fg_color=self.fg_color,
            bg_color=self.bg_color,
            hover_color=self.hover_color,
            corner_radius=self.corner_radius,
            border_width=self.border_width,
            border_color=self.border_color,
            separator_color=self.separator_color,
            text_color=self.text_color,
            font=self.font)
        
        submenu_button_seed.set_submenu(submenu=submenu)
        submenu_button_seed.configure(command=submenu.toggle_show)
        submenu.bind("<Enter>", lambda e: submenu._show_submenu(self, hovered=True))
        submenu_button_seed.bind("<Enter>", lambda e: self.after(150, lambda: submenu._show_submenu(self)))
        # submenu_button_seed.bind("<Leave>", lambda e: self.after(500, lambda: submenu._left(self)))
        submenu_button_seed.configure(cursor=self.cursor)
        
        submenu_button_seed.pack(
            side="top",
            fill="both", 
            expand=True,
            padx=3+(self.corner_radius/5),
            pady=3+(self.corner_radius/5))
        return submenu

    # @staticmethod
    # def _left(parent) -> None:
    #     if parent.hovered:
    #         return
    #     sub_menus = parent.get_sub_menus()
    #     for i in sub_menus:
    #         i._hide()

    def _show_submenu(self, parent, hovered=False) -> None:
        parent.hovered = hovered
        sub_menus = parent.get_sub_menus()
        for i in sub_menus:
            i._hide()
        self._show()

    def add_separator(self) -> None:
        separator = customtkinter.CTkFrame(
            master=self, 
            height=2,
            width=self.width,
            fg_color=self.separator_color, 
            border_width=0
        )
        separator.pack(
            side="top",
            fill="x",
            expand=True,
        )

    def _show(self, *args, **kwargs) -> None:
        dpi = self._get_widget_scaling()
        if isinstance(self.menu_seed_object, _CDMSubmenuButton):
            self.place(
                in_=self.menu_seed_object.parent_menu,
                x=(self.menu_seed_object.winfo_x() + self.menu_seed_object.winfo_width())/dpi + self.padx + 1,
                y=(self.menu_seed_object.winfo_y())/dpi - self.pady + 10)

        else:
            self.place(
                x=self.menu_seed_object.winfo_x()/dpi + self.padx,
                y=(self.menu_seed_object.winfo_y() + self.menu_seed_object.winfo_height())/dpi + self.pady)
        self.lift()
        self.focus()
        
    def _hide(self, *args, **kwargs) -> None:
        self.place_forget()
        
    def _hide_parent_menus(self, *args, **kwargs) -> None:
        if isinstance(self.menu_seed_object, _CDMSubmenuButton):
            self.menu_seed_object.parent_menu._hide_parent_menus()
            self.menu_seed_object.parent_menu._hide()
            
    def _hide_children_menus(self, *args, **kwargs) -> None:
        if any(isinstance(option, _CDMSubmenuButton) for option in self._options_list):
            for option in self._options_list:
                if isinstance(option, _CDMSubmenuButton):
                    option.submenu._hide()
                    
    def _hide_all_menus(self, *args, **kwargs) -> None:
        self._hide_children_menus()
        self._hide()
        self._hide_parent_menus()
        
    def _collapse_sibling_submenus(self, button: _CDMOptionButton | _CDMSubmenuButton, *args, **kwargs) -> None:
        for option in self._options_list:
            if option != button and isinstance(option, _CDMSubmenuButton):
                option.submenu._hide_children_menus()
                option.submenu._hide()

    def toggle_show(self, *args, **kwargs) -> None:
        widget_base = self.menu_seed_object.master.winfo_name()
        if widget_base.startswith("!ctktitlemenu") or widget_base.startswith("!ctkmenubar"):
            for i in self.menu_seed_object.master.menu:
                i._hide()
            
        if not self.winfo_manager():
            self._show()
            self.lift()
        else:
            self._hide_children_menus()
            self._hide()

    def _configure_button(self, button: customtkinter.CTkButton) -> None:
        button.configure(fg_color="transparent")
        if self.fg_color:
            button.configure(fg_color=self.fg_color)
        if self.hover_color:
            button.configure(hover_color=self.hover_color)
        # if self.font:
            # button.configure(font=self.font)

        button.bind("<Enter>", partial(self._collapse_sibling_submenus, button))
        
    def get_sub_menus(self) -> list["CustomDropdownMenu"]:
        if any(isinstance(option, _CDMSubmenuButton) for option in self._options_list):
            sub_menus_list = list()
            for option in self._options_list: 
                if isinstance(option, _CDMSubmenuButton):
                    sub_menus_list.append(option.submenu)
            return sub_menus_list
        else:
            return []

    def _get_coordinates(self, x_root, y_root) -> bool:
        return self.winfo_rootx() < x_root < self.winfo_rootx()+self.winfo_width() and \
            self.winfo_rooty() < y_root < self.winfo_rooty()+self.winfo_height()
    
    def _check_if_mouse_left(self, event: tk.Event = None) -> None:
        if not self.winfo_viewable():
            return
        
        if not self._get_coordinates(event.x_root, event.y_root):
            if (isinstance(self.menu_seed_object,
                           _CDMSubmenuButton) and not self.menu_seed_object.parent_menu._get_coordinates(event.x_root,
                                                                                                         event.y_root)):
                sub_menus = self.get_sub_menus()
                if sub_menus == [] or all((not submenu._get_coordinates(event.x_root, event.y_root))
                                          for submenu in sub_menus):
                    self._hide_all_menus()
            
            elif not isinstance(self.menu_seed_object, _CDMSubmenuButton):
                sub_menus = self.get_sub_menus()
                if sub_menus == [] or all((not submenu._get_coordinates(event.x_root, event.y_root))
                                          for submenu in sub_menus):
                    self._hide_all_menus()

    def get_list_menu(self) -> list:
        return self._options_list
