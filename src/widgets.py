# -*- coding: utf-8 -*-
import sys
import tkinter as tk
from typing import Any, Literal, Optional, Tuple, Union

import customtkinter as ctk
from PIL import ImageTk


class PatchedScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        """Initialize the Patched Scrollable Frame."""
        super().__init__(*args, **kwargs)

        # add missing bindings
        self.bind_all("<Button-4>", self._mouse_wheel_all, add="+")
        self.bind_all("<Button-5>", self._mouse_wheel_all, add="+")

    def _mouse_wheel_all(self, event: tk.Event) -> None:
        """
        Handle mouse wheel events for scrolling.

        Parameters:
            event (tk.Event): The mouse wheel event.
        """
        if self.check_if_master_is_canvas(event.widget):
            if sys.platform.startswith("win"):
                if self._shift_pressed:
                    if self._parent_canvas.xview() != (0.0, 1.0):
                        self._parent_canvas.xview("scroll", -int(event.delta / 6), "units")
                else:
                    if self._parent_canvas.yview() != (0.0, 1.0):
                        self._parent_canvas.yview("scroll", -int(event.delta / 6), "units")
            elif sys.platform == "darwin":
                if self._shift_pressed:
                    if self._parent_canvas.xview() != (0.0, 1.0):
                        self._parent_canvas.xview("scroll", -event.delta, "units")
                else:
                    if self._parent_canvas.yview() != (0.0, 1.0):
                        self._parent_canvas.yview("scroll", -event.delta, "units")
            else:
                if self._shift_pressed:
                    if self._parent_canvas.xview() != (0.0, 1.0):
                        if event.num == 4:
                            self._parent_canvas.xview_scroll(-1, "units")
                        elif event.num == 5:
                            self._parent_canvas.xview_scroll(1, "units")
                else:
                    if self._parent_canvas.yview() != (0.0, 1.0):
                        if event.num == 4:
                            self._parent_canvas.yview_scroll(-1, "units")
                        elif event.num == 5:
                            self._parent_canvas.yview_scroll(1, "units")

    def _reset_scrolling(self) -> None:
        """Reset the scrolling behavior of the canvas."""
        # Set the scrollbar position to the top
        self._scrollbar.set(0., 1.)

        # Fit the frame dimensions to the canvas
        self._fit_frame_dimensions_to_canvas(None)

        # Configure the canvas scroll region to fit the contents
        self._parent_canvas.configure(scrollregion=self._parent_canvas.bbox("all"))


class CollapsableFrame(ctk.CTkFrame):
    """Collapsible Frame Class."""

    def __init__(
            self,
            parent: Any,
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
            button_image: Union[ctk.CTkImage, ImageTk.PhotoImage, None] = None,
            button_hover: bool = True,
            button_compound: str = "left",
    ) -> None:
        """
        Initialize the Collapsible Frame.

        Parameters:
            parent (Any): The parent widget.
            alignment (Literal["left", "right"]): The alignment of the hide button.
            expanded (bool, optional): Whether the frame is initially expanded.
            Default is True.
            corner_radius (Optional[Union[int, str]], optional): The corner radius of the frame.
            Default is None.
            border_width (Optional[Union[int, str]], optional): The border width of the frame.
            Default is None.
            bg_color (Union[str, Tuple[str, str]], optional): The background color of the frame.
            Default is "transparent".
            fg_color (Optional[Union[str, Tuple[str, str]]], optional): The foreground color of the frame.
            Default is None.
            border_color (Optional[Union[str, Tuple[str, str]]], optional): The border color of the frame.
            Default is None.
            button_corner_radius (Optional[Union[int, str]], optional): The corner radius of the hide button.
            Default is None.
            button_border_width (Optional[Union[int, str]], optional): The border width of the hide button.
            Default is None.
            button_fg_color (Optional[Union[str, Tuple[str, str]]], optional): The foreground color of the hide button.
            Default is None.
            button_hover_color (Optional[Union[str, Tuple[str, str]]], optional): The hover color of the hide button.
            Default is None.
            button_border_color (Optional[Union[str, Tuple[str, str]]], optional): The border color of the hide button.
            Default is None.
            button_text_color (Optional[Union[str, Tuple[str, str]]], optional): The text color of the hide button.
            Default is None.
            button_image (Union[ctk.CTkImage, ImageTk.PhotoImage, None], optional): The image of the hide button.
            Default is None.
            button_hover (bool, optional): Whether the hide button should have a hover effect.
            Default is True.
            button_compound (str, optional): The compound style of the hide button.
            Default is "left".
        """
        # container
        self._parent_frame = ctk.CTkFrame(
            master=parent,
            corner_radius=corner_radius,
            border_width=border_width,
            bg_color=bg_color,
            fg_color=fg_color,
            border_color=border_color,
        )

        super().__init__(master=self._parent_frame, fg_color="transparent")

        # data
        self.expanded = expanded
        if alignment == "left":
            self.char = ("<", ">")
        elif alignment == "right":
            self.char = (">", "<")
        else:
            raise KeyError("alignment must be either 'left' or 'right'")

        # widgets
        start_char = self.char[0] if self.expanded else self.char[1]
        self._hide_button = ctk.CTkButton(
            master=self._parent_frame,
            text=start_char,
            width=20,
            height=50,
            corner_radius=button_corner_radius,
            border_width=button_border_width,
            fg_color=button_fg_color,
            hover_color=button_hover_color,
            border_color=button_border_color,
            text_color=button_text_color,
            image=button_image,
            hover=button_hover,
            compound=button_compound,
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
        """
        Hide the widget by forgetting it and updating the hide button.

        Returns:
            None
        """
        self.expanded = False
        super().pack_forget()
        self._hide_button.configure(text=self.char[1], command=self._show)
        self.update()

    def _show(self) -> None:
        """
        Show the widget by packing it with expand and fill options, and updating the hide button.

        Returns:
            None
        """
        self.expanded = True
        super().pack(expand=True, fill="both")
        self._hide_button.configure(text=self.char[0], command=self._hide)
        self.update()

    def configure(self, **kwargs) -> None:
        """
        Configure the appearance and settings of the widget.

        Keyword Arguments:
            button_corner_radius (int): The corner radius of the button.
            button_border_width (int): The border width of the button.
            button_fg_color (str): The foreground color of the button.
            button_hover_color (str): The hover color of the button.
            button_border_color (str): The border color of the button.
            button_text_color (str): The text color of the button.
            button_image (str): The image of the button.
            button_hover (bool): Whether the button should have a hover effect.
            button_compound (str): The compound style of the button.

        Returns:
            None
        """
        if "button_corner_radius" in kwargs:
            self._hide_button.configure(
                corner_radius=kwargs.pop("button_corner_radius")
            )

        if "button_border_width" in kwargs:
            self._hide_button.configure(
                border_width=kwargs.pop("button_border_width"))

        if "button_fg_color" in kwargs:
            self._hide_button.configure(fg_color=kwargs.pop("button_fg_color"))

        if "button_hover_color" in kwargs:
            self._hide_button.configure(
                hover_color=kwargs.pop("button_hover_color"))

        if "button_border_color" in kwargs:
            self._hide_button.configure(
                border_color=kwargs.pop("button_border_color"))

        if "button_text_color" in kwargs:
            self._hide_button.configure(
                text_color=kwargs.pop("button_text_color"))

        if "button_image" in kwargs:
            self._hide_button.configure(image=kwargs.pop("button_image"))

        if "button_hover" in kwargs:
            self._hide_button.configure(hover=kwargs.pop("button_hover"))

        if "button_compound" in kwargs:
            self._hide_button.configure(compound=kwargs.pop("button_compound"))

        self._parent_frame.configure(**kwargs)

    def pack(self, **kwargs) -> None:
        """
        Pack the widget using the pack geometry manager.

        Keyword Arguments:
            Same as the pack method in tkinter.

        Returns:
            None
        """
        self._parent_frame.pack(**kwargs)

    def place(self, **kwargs) -> None:
        """
        Place the widget using the place geometry manager.

        Keyword Arguments:
            Same as the place method in tkinter.

        Returns:
            None
        """
        self._parent_frame.place(**kwargs)

    def grid(self, **kwargs) -> None:
        """
        Grid the widget using the grid geometry manager.

        Keyword Arguments:
            Same as the grid method in tkinter.

        Returns:
            None
        """
        self._parent_frame.grid(**kwargs)

    def pack_forget(self) -> None:
        """
        Forget the widget packed using the pack geometry manager.

        Returns:
            None
        """
        self._parent_frame.pack_forget()

    def place_forget(self) -> None:
        """
        Forget the widget placed using the place geometry manager.

        Returns:
            None
        """
        self._parent_frame.place_forget()

    def grid_forget(self) -> None:
        """
        Forget the widget gridded using the grid geometry manager.

        Returns:
            None
        """
        self._parent_frame.grid_forget()

    def grid_remove(self) -> None:
        """
        Remove the widget from the grid.

        Returns:
            None
        """
        self._parent_frame.grid_remove()

    def grid_propagate(self, **kwargs) -> None:
        """
        Enable or disable the propagation of the widget's dimensions in the grid.

        Keyword Arguments:
            Same as the grid_propagate method in tkinter.

        Returns:
            None
        """
        self._parent_frame.grid_propagate(**kwargs)

    def grid_info(self):
        """
        Retrieve information about the widget's grid placement.

        Returns:
            Same as the grid_info method in tkinter.
        """
        return self._parent_frame.grid_info()

    def lift(self, aboveThis: Any = None) -> None:
        """
        Raise the widget to the top of the stacking order.

        Parameters:
            aboveThis (Any): The widget above which to lift the current widget.

        Returns:
            None
        """
        self._parent_frame.lift(aboveThis)

    def lower(self, belowThis: Any = None) -> None:
        """
        Lower the widget to the bottom of the stacking order.

        Parameters:
            belowThis (Any): The widget below which to lower the current widget.

        Returns:
            None
        """
        self._parent_frame.lower(belowThis)


if __name__ == "__main__":
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

    ctk.CTkLabel(collapsable_frame, text="Test Label").pack(
        fill="x", expand=True)
    ctk.CTkButton(collapsable_frame, text="Test Button").pack(
        fill="x", expand=True)

    # debugging scrollable frame
    scrollable_frame = ctk.CTkScrollableFrame(window)  # , orientation="auto")
    scrollable_frame.pack(side="left", expand=True, fill="both")
    # scrollable_frame.grid(column=1, row=0, sticky="news")

    for i in range(50):
        tmp = ctk.CTkLabel(scrollable_frame, text=f"text {i}")
        tmp.pack(fill="x", expand=True)
        # tmp.pack(side="left", fill="y", expand=True)

    window.mainloop()
