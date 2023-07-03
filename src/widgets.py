# -*- coding: utf-8 -*-
import platform
import tkinter as tk
from typing import Any, Literal, Optional, Tuple, Union

import customtkinter as ctk
from PIL import ImageTk
from customtkinter.windows.widgets.appearance_mode import CTkAppearanceModeBaseClass
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass
from customtkinter.windows.widgets.scaling import CTkScalingBaseClass


class ScrollableFrame(tk.Frame, CTkAppearanceModeBaseClass, CTkScalingBaseClass):
    """Cross-platform Scrollable Frame Class."""

    def __init__(
            self,
            parent: Any,
            corner_radius: Optional[Union[int, str]] = None,
            border_width: Optional[Union[int, str]] = None,
            bg_color: Union[str, Tuple[str, str]] = "transparent",
            fg_color: Optional[Union[str, Tuple[str, str]]] = None,
            border_color: Optional[Union[str, Tuple[str, str]]] = None,
            scrollbar_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
            scrollbar_button_color: Optional[Union[str, Tuple[str, str]]] = None,
            scrollbar_button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
            direction: Literal["x", "y", "both", "auto"] = "y"
    ) -> None:
        """
        Scrollable Frame supporting scrolling in x and y direction on every system.
        :param parent: Root widget
        :param corner_radius: Corner radius in px
        :param border_width: Border width in px
        :param bg_color:
        :param fg_color:
        :param border_color:
        :param scrollbar_fg_color:
        :param scrollbar_button_color:
        :param scrollbar_button_hover_color:
        :param direction:
        """
        # data
        self.direction_mode = direction
        if self.direction_mode in ["x", "y", "both", "auto"]:
            self.x_scrollable = self.direction_mode in ["x", "both"]
            self.y_scrollable = self.direction_mode in ["y", "both"]
        else:
            raise ValueError("Direction must be 'x', 'y', 'both' or 'auto'")

        # widgets
        # container widgets
        self._parent_frame = ctk.CTkFrame(
            master=parent,
            corner_radius=corner_radius,
            border_width=border_width,
            bg_color=bg_color,
            fg_color=fg_color,
            border_color=border_color
        )

        self._canvas = tk.Canvas(
            master=self._parent_frame,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        # scrollbars
        self._y_scrollbar = ctk.CTkScrollbar(
            master=self._parent_frame,
            orientation="vertical",
            command=self._canvas.yview,
            fg_color=scrollbar_fg_color,
            button_color=scrollbar_button_color,
            button_hover_color=scrollbar_button_hover_color
        )
        self._canvas.configure(yscrollcommand=self._y_scrollbar.set)

        self._x_scrollbar = ctk.CTkScrollbar(
            master=self._parent_frame,
            orientation="horizontal",
            command=self._canvas.xview,
            fg_color=scrollbar_fg_color,
            button_color=scrollbar_button_color,
            button_hover_color=scrollbar_button_hover_color
        )
        self._canvas.configure(xscrollcommand=self._x_scrollbar.set)

        tk.Frame.__init__(self, master=self._canvas, highlightthickness=0)
        CTkAppearanceModeBaseClass.__init__(self)
        CTkScalingBaseClass.__init__(self, scaling_type="widget")

        self._canvas_window = self._canvas.create_window(
            (0, 0), window=self, anchor="nw"
        )

        # layout
        self._parent_frame.grid_columnconfigure(0, weight=1)
        self._parent_frame.grid_rowconfigure(0, weight=1)

        self._canvas.grid(column=0, row=0, sticky="news")
        self._update_direction()

        # events
        # These functions prevent the canvas from scrolling unless the cursor is in it
        self._canvas.bind("<Enter>", self._enter_frame)
        self._canvas.bind("<Leave>", self._leave_frame)

        self.bind("<Configure>", self._on_frame_configure)
        self._canvas.bind("<Configure>", self._on_canvas_configure)

        if self._parent_frame.cget("fg_color") == "transparent":
            tk.Frame.configure(self, bg=self._apply_appearance_mode(self._parent_frame.cget("bg_color")))
            self._canvas.configure(bg=self._apply_appearance_mode(self._parent_frame.cget("bg_color")))
        else:
            tk.Frame.configure(self, bg=self._apply_appearance_mode(self._parent_frame.cget("fg_color")))
            self._canvas.configure(bg=self._apply_appearance_mode(self._parent_frame.cget("fg_color")))

    def _on_frame_configure(self, _event: tk.Event) -> None:
        """Called when the viewport size changed."""
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_configure(self, event: tk.Event) -> None:
        """Called when the canvas size changed."""
        canvas_bbox = self._canvas.bbox(self._canvas_window)

        self._x_scrollbar.update()
        self._y_scrollbar.update()

        if self.direction_mode == "auto":
            # TODO: preserve inner frame size when scrollbars are added
            print(
                f"Widget: {event.widget} - width: {event.width} ({canvas_bbox[2]}); "
                f"height: {event.height} ({canvas_bbox[3]})"
            )
            self.x_scrollable = (event.width - self._y_scrollbar.winfo_width()) < canvas_bbox[2]
            self.y_scrollable = (event.height - self._x_scrollbar.winfo_height()) < canvas_bbox[3]

        elif self.direction_mode == "x":
            self._canvas.itemconfigure(self._canvas_window, height=self._canvas.winfo_height())

        elif self.direction_mode == "y":
            self._canvas.itemconfigure(self._canvas_window, width=self._canvas.winfo_width())

        if event.width > canvas_bbox[2]:
            if self.y_scrollable:
                self._canvas.itemconfigure(
                    self._canvas_window, width=(event.width - self._y_scrollbar.winfo_width())
                )
            else:
                self._canvas.itemconfigure(self._canvas_window, width=event.width)

        if event.height > canvas_bbox[3]:
            if self.x_scrollable:
                self._canvas.itemconfigure(
                    self._canvas_window, height=(event.height - self._x_scrollbar.winfo_height())
                )
            else:
                self._canvas.itemconfigure(self._canvas_window, height=event.height)

        self._update_direction()

    def _update_direction(self) -> None:
        """Update the scroll direction of the frame."""
        self._y_scrollbar.grid_forget()
        self._x_scrollbar.grid_forget()

        if self.y_scrollable:
            self._y_scrollbar.grid(row=0, column=1, sticky="news")
        if self.x_scrollable:
            self._x_scrollbar.grid(row=1, column=0, sticky="news")

    def _on_mouse_wheel(self, event: tk.Event) -> None:
        """Cross-platform scroll-wheel event."""
        if platform.system() == "Windows":
            self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == "Darwin":
            self._canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self._canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self._canvas.yview_scroll(1, "units")

    def _on_shift_mouse_wheel(self, event: tk.Event) -> None:
        """Scroll horizontally while holding shift."""
        if platform.system() == "Windows":
            self._canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == "Darwin":
            self._canvas.xview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self._canvas.xview_scroll(-1, "units")
            elif event.num == 5:
                self._canvas.xview_scroll(1, "units")

    def _enter_frame(self, _event: tk.Event) -> None:
        """Bind all scrolling events when entering frame."""
        if platform.system() == "Linux":
            if self.y_scrollable:
                self._canvas.bind_all("<Button-4>", self._on_mouse_wheel)
                self._canvas.bind_all("<Button-5>", self._on_mouse_wheel)
            if self.x_scrollable:
                self._canvas.bind_all("<Shift-Button-4>", self._on_shift_mouse_wheel)
                self._canvas.bind_all("<Shift-Button-5>", self._on_shift_mouse_wheel)
        else:
            if self.y_scrollable:
                self._canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)
            if self.x_scrollable:
                self._canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mouse_wheel)

    def _leave_frame(self, _event: tk.Event) -> None:
        """Unbind all scrolling events when leaving frame."""
        if platform.system() == "Linux":
            if self.y_scrollable:
                self._canvas.unbind_all("<Button-4>")
                self._canvas.unbind_all("<Button-5>")
            if self.x_scrollable:
                self._canvas.unbind_all("<Shift-Button-4>")
                self._canvas.unbind_all("<Shift-Button-5>")
        else:
            if self.y_scrollable:
                self._canvas.unbind_all("<MouseWheel>")
            if self.x_scrollable:
                self._canvas.unbind_all("<Shift-MouseWheel>")

    def _set_appearance_mode(self, mode_string: str) -> None:
        super()._set_appearance_mode(mode_string)

        if self._parent_frame.cget("fg_color") == "transparent":
            tk.Frame.configure(self, bg=self._apply_appearance_mode(self._parent_frame.cget("bg_color")))
            self._canvas.configure(bg=self._apply_appearance_mode(self._parent_frame.cget("bg_color")))
        else:
            tk.Frame.configure(self, bg=self._apply_appearance_mode(self._parent_frame.cget("fg_color")))
            self._canvas.configure(bg=self._apply_appearance_mode(self._parent_frame.cget("fg_color")))

    def configure(self, **kwargs) -> None:
        if "corner_radius" in kwargs:
            new_corner_radius = kwargs.pop("corner_radius")
            self._parent_frame.configure(corner_radius=new_corner_radius)

        if "border_width" in kwargs:
            self._parent_frame.configure(border_width=kwargs.pop("border_width"))

        if "fg_color" in kwargs:
            self._parent_frame.configure(fg_color=kwargs.pop("fg_color"))

            if self._parent_frame.cget("fg_color") == "transparent":
                tk.Frame.configure(self, bg=self._apply_appearance_mode(self._parent_frame.cget("bg_color")))
                self._canvas.configure(bg=self._apply_appearance_mode(self._parent_frame.cget("bg_color")))
            else:
                tk.Frame.configure(self, bg=self._apply_appearance_mode(self._parent_frame.cget("fg_color")))
                self._canvas.configure(bg=self._apply_appearance_mode(self._parent_frame.cget("fg_color")))

            for child in self.winfo_children():
                if isinstance(child, CTkBaseClass):
                    child.configure(bg_color=self._parent_frame.cget("fg_color"))

        if "scrollbar_fg_color" in kwargs:
            self._x_scrollbar.configure(fg_color=kwargs.pop("scrollbar_fg_color"))
            self._y_scrollbar.configure(fg_color=kwargs.pop("scrollbar_fg_color"))

        if "scrollbar_button_color" in kwargs:
            self._x_scrollbar.configure(button_color=kwargs.pop("scrollbar_button_color"))
            self._y_scrollbar.configure(button_color=kwargs.pop("scrollbar_button_color"))

        if "scrollbar_button_hover_color" in kwargs:
            self._x_scrollbar.configure(button_hover_color=kwargs.pop("scrollbar_button_hover_color"))
            self._y_scrollbar.configure(button_hover_color=kwargs.pop("scrollbar_button_hover_color"))

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

    def destroy(self):
        tk.Frame.destroy(self)
        CTkAppearanceModeBaseClass.destroy(self)
        CTkScalingBaseClass.destroy(self)


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
    scrollable_frame = ScrollableFrame(window, direction="auto")
    scrollable_frame.pack(side="left", expand=True, fill="both")
    # scrollable_frame.grid(column=1, row=0, sticky="news")

    for i in range(50):
        tmp = ctk.CTkLabel(scrollable_frame, text=f"text {i}")
        tmp.pack(fill="x", expand=True)
        # tmp.pack(side="left", fill="y", expand=True)

    window.mainloop()
