import customtkinter


class CTkPopupMenu(customtkinter.CTkFrame):
    def __init__(self,
                 master,
                 width=170,
                 height=25,
                 text_color=None,
                 hover_color=("grey75", "grey25"),   # None,
                 hover: bool = True,
                 border_width: int = 1,
                 values: tuple = (),
                 font=None,
                 corner_radius: int = 5,
                 separator_color: str | tuple[str, str] = ("grey80", "grey20"),
                 **kwargs):
        
        super().__init__(master.winfo_toplevel(), border_width=border_width, width=width,
                         corner_radius=corner_radius, **kwargs)

        self.text_color = customtkinter.ThemeManager.theme["CTkLabel"]["text_color"] \
            if text_color is None else text_color
        self.hover_color = customtkinter.ThemeManager.theme["CTkButton"]["hover_color"] \
            if hover_color is None else hover_color
        self.corner_radius = corner_radius
        self.hover = hover
        self.values = values
        self.widget = master
        self.height = height
        self.width = width
        self.separator_color = separator_color
        
        if not font:
            self.font = customtkinter.CTkFont(customtkinter.ThemeManager.theme["CTkFont"]["family"],
                                              customtkinter.ThemeManager.theme["CTkFont"]["size"])
        else:
            if isinstance(font, customtkinter.CTkFont):
                self.font = font
            else:
                self.font = customtkinter.CTkFont(*font)
                
        for i in self.values:
            self.add_buttons(text=i['text'], image=i.get('image', None),
                             compound='left', command=i.get('command', None))

        self.widget.bind("<Button-3>", lambda event: self.popup(event), add="+")      # right click mouse bind
        self.widget.winfo_toplevel().bind("<Button-1>", lambda event: self.hide(), add="+")
        self.widget.bind("<FocusOut>", lambda event: self.hide(), add="+")
        self.widget.bind("<Configure>", lambda event: self.hide())
        self.bind("<Button-1>", lambda event: self.hide())
        # self.widget.bind("<Destroy>", lambda event: self.destroy())
        
        self.dpi = self._get_widget_scaling()
        
    def add_buttons(self, text, command, **kwargs) -> None:
        button = customtkinter.CTkButton(self, height=self.height, width=self.width, text=text, command=command,
                                         fg_color="transparent", corner_radius=self.corner_radius,
                                         text_color=self.text_color,
                                         hover=self.hover, hover_color=self.hover_color, border_width=0,
                                         anchor="w", font=self.font,
                                         **kwargs)
        button.pack(padx=5, pady=5)
        button.bind("<Button-1>", lambda event: self.hide(), add="+")

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
        
    def clear_all(self) -> None:
        for i in self.winfo_children():
            i.destroy()

    def configure(self, **kwargs) -> None:
        if "values" in kwargs:
            self.values = kwargs.pop("values")
            
        if "image" in kwargs:
            self.images = kwargs.pop("images")
        
        if "text_color" in kwargs:
            self.text_color = kwargs.pop("text_color")

        if "hover_color" in kwargs:
            self.hover_color = kwargs.pop("hover_color")

        if "hover" in kwargs:
            self.hover = kwargs.pop("hover")

        if "corner_radius" in kwargs:
            self.corner_radius = kwargs["corner_radius"]

        if "font" in kwargs:
            self.font = kwargs.pop("font")

        super().configure(**kwargs)
        
        self.clear_all()
        
        for i in self.values:
            if i:
                self.add_buttons(text=i['text'], image=i.get('image', ''), compound='left',
                                 command=i.get('command', None))
            else:
                self.add_separator()

    def cget(self, param) -> str:
        if param == "values":
            return self.values
        if param == "text_color":
            return self.text_color
        if param == "hover_color":
            return self.hover_color
        if param == "hover":
            return self.hover
        if param == "font":
            return self.font
        return super().cget(param)

    def destroy(self) -> None:
        super().destroy()
        
    def popup(self, event) -> None:
        # print(self.widget.winfo_pointerxy())    # коорд мыши относительно экрана компа (x, y)
        # print(self.widget.winfo_x(), self.widget.winfo_y()) # коорд окна относительно экрана компа
        # print(self.widget.winfo_rootx(), self.widget.winfo_rooty())
        # print(event.x, event.y)
        # x = int((self.widget.winfo_pointerx() - self.widget.winfo_rootx()) / self.dpi) + 10
        # y = int((self.widget.winfo_pointery() - self.widget.winfo_rooty()) / self.dpi) + 10
        # x = self.widget.winfo_x() - self.winfo_reqwidth() - 5
        # y = self.widget.winfo_y() - self.winfo_reqheight() - 5
        # print(self.winfo_x(), self.winfo_y())

        x = (event.x + self.widget.winfo_x()) / self.dpi + 10
        y = (event.y + self.widget.winfo_y() + 140) / self.dpi + 10
        # print(x, y)
        # print(self.widget.winfo_geometry())
        # print(self.winfo_geometry())
        self.widget.unbind("<Configure>")    
        self.place(x=x, y=y)
        self.focus()
        self.lift()
        self.after(300, self.bind_configure)
        
    def bind_configure(self, arg=None) -> None:
        self.widget.bind("<Configure>", lambda event: self.hide())
        
    def hide(self) -> None:
        # print('hide')
        if self.widget.winfo_exists():
            if self.winfo_ismapped():
                self.place_forget()
                