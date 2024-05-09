import customtkinter as ctk


class Separator(ctk.CTkFrame):

    def __init__(self,
                 master,
                 orient="horizontal",
                 border_width=0,
                 fg_color=("grey65", "grey35"),
                 height=2,
                 width=2,
                 **kwargs
                 ):
        if orient == "horizontal":
            width = master.cget('width')
            # height = 2
        elif orient == "vertical":
            height = master.cget('height')
            # width = 2
            
        super().__init__(
                master=master,
                width=width,
                height=height,
                border_width=border_width,
                fg_color=fg_color,
                **kwargs
                )
                