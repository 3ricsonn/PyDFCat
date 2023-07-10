# -*- coding: utf-8 -*-
from typing import Any, Literal, Optional, Tuple, Union

import customtkinter as ctk
from PIL import ImageTk


class CollapsableFrame(ctk.CTkFrame):
    """Collapsible Frame Class."""

    def __init__(
            self, parent: Any,
            alignment: Literal["left", "right"],
            expanded: bool = True,
            corner_radius: Optional[Union[int, str]] = None,
            border_width: Optional[Union[int, str]] = None,
            bg_color: Union[str, Tuple[str, str]] = "transparent",
            fg_color: Optional[Union[str, Tuple[str, str]]] = None,
            border_color: Optional[Union[str, Tuple[str, str]]] = None,
            button_corner_radius: Optional[Union[int, str]] = None,
            button_border_width: Optional[Union[int, str]] = None,
            button_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
            button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
            button_border_color: Optional[Union[str, Tuple[str, str]]] = None,
            button_text_color: Optional[Union[str, Tuple[str, str]]] = None,
            button_image: Union[ctk.CTkImage, "ImageTk.PhotoImage", None] = None,
            button_hover: bool = True,
            button_compound: str = "left",
    ) -> None:
        """

        :param parent: root widget
        :param alignment: collapse to the 'left' or 'right'
        :param expanded: is frame is expanded odr collapse by creation
        :param corner_radius:
        :param border_width:
        :param bg_color:
        :param fg_color:
        :param border_color:
        :param button_corner_radius:
        :param button_border_width:
        :param button_fg_color:
        :param button_hover_color:
        :param button_border_color:
        :param button_text_color:
        :param button_image:
        :param button_hover:
        :param button_compound:
        """
        # container
        self._parent_frame = ctk.CTkFrame(
            master=parent,
            corner_radius=corner_radius,
            border_width=border_width,
            bg_color=bg_color,
            fg_color=fg_color,
            border_color=border_color
        )

        super().__init__(master=self._parent_frame, fg_color="transparent")

        # data
        self.expanded = expanded
        if alignment == "left":
            self.char = ("<", ">")
        elif alignment == "right":
            self.char = (">", "<")
        else:
            raise KeyError("alignment mus be ether 'left' or 'right'")

        # widgets
        start_char = self.char[0] if self.expanded else self.char[1]
        self._hide_button = ctk.CTkButton(
            master=self._parent_frame,
            text=start_char,
            width=20, height=50,
            corner_radius=button_corner_radius,
            border_width=button_border_width,
            fg_color=button_fg_color,
            hover_color=button_hover_color,
            border_color=button_border_color,
            text_color=button_text_color,
            image=button_image,
            hover=button_hover,
            compound=button_compound
        )
        if alignment == "left":
            self._hide_button.pack(side="right")
        else:
            self._hide_button.pack(side="left")

        if self.expanded:
            self._show()
        else:
            self._hide()

    def _hide(self) -> None:
        self.expanded = False
        super().pack_forget()
        self._hide_button.configure(text=self.char[1], command=self._show)
        self.update()

    def _show(self) -> None:
        self.expanded = True
        super().pack(expand=True, fill="both")
        self._hide_button.configure(text=self.char[0], command=self._hide)
        self.update()

    def configure(self, **kwargs) -> None:

        if "button_corner_radius" in kwargs:
            self._hide_button.configure(corner_radius=kwargs.pop("button_corner_radius"))

        if "button_border_width" in kwargs:
            self._hide_button.configure(border_width=kwargs.pop("button_border_width"))

        if "button_fg_color" in kwargs:
            self._hide_button.configure(fg_color=kwargs.pop("button_fg_color"))

        if "button_hover_color" in kwargs:
            self._hide_button.configure(hover_color=kwargs.pop("button_hover_color"))

        if "button_border_color" in kwargs:
            self._hide_button.configure(border_color=kwargs.pop("button_border_color"))

        if "button_text_color" in kwargs:
            self._hide_button.configure(text_color=kwargs.pop("button_text_color"))

        if "button_image" in kwargs:
            self._hide_button.configure(image=kwargs.pop("button_image"))

        if "button_hover" in kwargs:
            self._hide_button.configure(hover=kwargs.pop("button_hover"))

        if "button_compound" in kwargs:
            self._hide_button.configure(compound=kwargs.pop("button_compound"))

        self._parent_frame.configure(**kwargs)

    def pack(self, **kwargs) -> None:
        self._parent_frame.pack(**kwargs)

    def place(self, **kwargs) -> None:
        self._parent_frame.place(**kwargs)

    def grid(self, **kwargs) -> None:
        self._parent_frame.grid(**kwargs)

    def pack_forget(self) -> None:
        self._parent_frame.pack_forget()

    def place_forget(self) -> None:
        self._parent_frame.place_forget()

    def grid_forget(self) -> None:
        self._parent_frame.grid_forget()

    def grid_remove(self) -> None:
        self._parent_frame.grid_remove()

    def grid_propagate(self, **kwargs) -> None:
        self._parent_frame.grid_propagate(**kwargs)

    def grid_info(self):
        return self._parent_frame.grid_info()

    def lift(self, aboveThis: Any = None) -> None:
        self._parent_frame.lift(aboveThis)

    def lower(self, belowThis: Any = None) -> None:
        self._parent_frame.lower(belowThis)


if __name__ == '__main__':
    window = ctk.CTk()
    window.geometry("400x200")
    ctk.set_appearance_mode("dark")

    # layout
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=0)
    window.columnconfigure(1, weight=1)

    # debugging collapsable frame
    collapsable_frame = CollapsableFrame(window, alignment="left")
    collapsable_frame.pack(side="left", expand=True, fill="both")
    # collapsable_frame.grid(column=0, row=0, sticky="news")

    ctk.CTkLabel(collapsable_frame, text="Test Label").pack(fill="x", expand=True)
    ctk.CTkButton(collapsable_frame, text="Test Button").pack(fill="x", expand=True)

    # debugging scrollable frame
    scrollable_frame = ctk.CTkScrollableFrame(window)  # , orientation="auto")
    scrollable_frame.pack(side="left", expand=True, fill="both")
    # scrollable_frame.grid(column=1, row=0, sticky="news")

    for i in range(50):
        tmp = ctk.CTkLabel(scrollable_frame, text=f"text {i}")
        tmp.pack(fill="x", expand=True)
        # tmp.pack(side="left", fill="y", expand=True)

    window.mainloop()
