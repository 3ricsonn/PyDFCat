# -*- coding: utf-8 -*-
import math
import sys
import tkinter as tk
from typing import Any, Literal, Optional, Tuple, Union

import customtkinter as ctk
import fitz  # PyMuPDF
from PIL import Image, ImageTk

from .settings import (
    COLOR_SELECTED_BLUE,
    PAGE_IPADDING,
    PAGE_X_PADDING,
    PAGE_Y_PADDING,
)


class CollapsableFrame(ctk.CTkFrame):
    """
    Collapsible Frame Class.

    This class is a custom Tkinter Frame that can collapse and expand its contents.
    """

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

        Args:
            parent (Any): The parent widget.
            alignment (Literal["left", "right"]):
                The alignment of the hide button, either "left" or "right".
            expanded (bool, optional):
                Whether the frame is initially expanded. Default is True.
            corner_radius (Optional[Union[int, str]], optional):
                The corner radius of the frame. Default is None.
            border_width (Optional[Union[int, str]], optional):
                The border width of the frame. Default is None.
            bg_color (Union[str, Tuple[str, str]], optional):
                The background color of the frame. Default is "transparent".
            fg_color (Optional[Union[str, Tuple[str, str]]], optional):
                The foreground color of the frame. Default is None.
            border_color (Optional[Union[str, Tuple[str, str]]], optional):
                The border color of the frame. Default is None.
            button_corner_radius (Optional[Union[int, str]], optional):
                The corner radius of the hide button. Default is None.
            button_border_width (Optional[Union[int, str]], optional):
                The border width of the hide button. Default is None.
            button_fg_color (Optional[Union[str, Tuple[str, str]]], optional):
                The foreground color of the hide button. Default is None.
            button_hover_color (Optional[Union[str, Tuple[str, str]]], optional):
                The hover color of the hide button. Default is None.
            button_border_color (Optional[Union[str, Tuple[str, str]]], optional):
                The border color of the hide button. Default is None.
            button_text_color (Optional[Union[str, Tuple[str, str]]], optional):
                The text color of the hide button. Default is None.
            button_image (Union[ctk.CTkImage, ImageTk.PhotoImage, None], optional):
                The image of the hide button. Default is None.
            button_hover (bool, optional):
                Whether the hide button should have a hover effect. Default is True.
            button_compound (str, optional):
                The compound style of the hide button. Default is "left".
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
            raise KeyError("alignment mus be ether 'left' or 'right'")

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
        """Hide the widget by forgetting it and updating the hide button."""
        self.expanded = False
        super().pack_forget()
        self._hide_button.configure(text=self.char[1], command=self._show)
        self.update()

    def _show(self) -> None:
        """Show the widget and updating the hide button."""
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
        """
        if "button_corner_radius" in kwargs:
            self._hide_button.configure(
                corner_radius=kwargs.pop("button_corner_radius")
            )

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
        """
        Pack the widget using the pack geometry manager.

        Keyword Arguments:
            Same as the pack method in tkinter.
        """
        self._parent_frame.pack(**kwargs)

    def place(self, **kwargs) -> None:
        """
        Place the widget using the place geometry manager.

        Keyword Arguments:
            Same as the place method in tkinter.
        """
        self._parent_frame.place(**kwargs)

    def grid(self, **kwargs) -> None:
        """
        Grid the widget using the grid geometry manager.

        Keyword Arguments:
            Same as the grid method in tkinter.
        """
        self._parent_frame.grid(**kwargs)

    def pack_forget(self) -> None:
        """Forget the widget packed using the pack geometry manager."""
        self._parent_frame.pack_forget()

    def place_forget(self) -> None:
        """Forget the widget placed using the place geometry manager."""
        self._parent_frame.place_forget()

    def grid_forget(self) -> None:
        """Forget the widget gridded using the grid geometry manager."""
        self._parent_frame.grid_forget()

    def grid_remove(self) -> None:
        """Remove the widget from the grid."""
        self._parent_frame.grid_remove()

    def grid_propagate(self, **kwargs) -> None:
        """
        Enable or disable the propagation of the widget's dimensions in the grid.

        Keyword Arguments:
            Same as the grid_propagate method in tkinter.
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
        """
        self._parent_frame.lift(aboveThis)

    def lower(self, belowThis: Any = None) -> None:
        """
        Lower the widget to the bottom of the stacking order.

        Parameters:
            belowThis (Any): The widget below which to lower the current widget.
        """
        self._parent_frame.lower(belowThis)


class DynamicScrollableFrame(ctk.CTkScrollableFrame):
    """
    An extension for the build-in customtkinter scrollable frame with dynamic placed scrollbars
    and patched mousewheel scrolling for linux

    This class inherits from ctk.CTkScrollableFrame.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Create a scrollable frame.

        Parameters:
            parent (Any): The parent widget.
            width (Optional[Union[int, float]]): The desired width of the frame.
            height (Optional[Union[int, float]]): The desired height of the frame.
            corner_radius (Optional[Union[int, str]]): The corner radius of the frame.
            border_width (Optional[Union[int, str]]): The border width of the frame.
            bg_color (Union[str, Tuple[str, str]]): The background color of the frame.
            fg_color (Optional[Union[str, Tuple[str, str]]]): The foreground color of the frame.
            border_color (Optional[Union[str, Tuple[str, str]]]): The border color of the frame.
            scrollbar_fg_color (Optional[Union[str, Tuple[str, str]]]):
                The foreground color of the scrollbars.
            scrollbar_button_color (Optional[Union[str, Tuple[str, str]]]):
                The color of the scrollbar buttons.
            scrollbar_button_hover_color (Optional[Union[str, Tuple[str, str]]]):
                The color of the scrollbar buttons when hovered.
            orientation (Literal["horizontal", "vertical", "both"]): The scrolling orientation.
        """
        super().__init__(*args, **kwargs)

        #
        if self._orientation == "horizontal":
            self._parent_canvas.configure(
                xscrollcommand=self._dynamic_horizontal_scrollbar
            )
        elif self._orientation == "vertical":
            self._parent_canvas.configure(
                yscrollcommand=self._dynamic_vertical_scrollbar
            )

        # events binding
        # These functions prevent the canvas from scrolling unless the cursor is in it
        self._parent_canvas.bind("<Enter>", self._enter_frame)
        self._parent_canvas.bind("<Leave>", self._leave_frame)

    def _dynamic_vertical_scrollbar(self, x: float, y: float) -> None:
        """
        Dynamically handle the vertical scrollbar.

        Parameters:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
        """
        if float(x) == 0.0 and float(y) == 1.0:
            self._scrollbar.grid_forget()
        else:
            self._create_grid()
        self._scrollbar.set(x, y)

    def _dynamic_horizontal_scrollbar(self, x: float, y: float) -> None:
        """
        Dynamically handle the horizontal scrollbar.

        Parameters:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
        """
        if float(x) == 0.0 and float(y) == 1.0:
            self._scrollbar.grid_forget()
        else:
            self._create_grid()
        self._scrollbar.set(x, y)

    def _on_mouse_wheel(self, event: tk.Event) -> None:
        """
        Handle mouse wheel events for vertical scrolling.

        Parameters:
            event (tk.Event): The mouse wheel event.
        """
        if self._parent_canvas.yview() != (0.0, 1.0):
            if sys.platform.startswith("win"):
                self._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif sys.platform == "darwin":
                self._parent_canvas.yview_scroll(int(-1 * event.delta), "units")
            else:
                if event.num == 4:
                    self._parent_canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    self._parent_canvas.yview_scroll(1, "units")

    def _on_shift_mouse_wheel(self, event: tk.Event) -> None:
        """
        Handle mouse wheel events for horizontal scrolling while holding the shift key.

        Parameters:
            event (tk.Event): The mouse wheel event.
        """
        if self._parent_canvas.xview() != (0.0, 1.0):
            if sys.platform.startswith("win"):
                self._parent_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
            elif sys.platform == "darwin":
                self._parent_canvas.xview_scroll(int(-1 * event.delta), "units")
            else:
                if event.num == 4:
                    self._parent_canvas.xview_scroll(-1, "units")
                elif event.num == 5:
                    self._parent_canvas.xview_scroll(1, "units")

    def _enter_frame(self, _event: tk.Event) -> None:
        """
        Bind scrolling events when entering the frame.

        Parameters:
            _event (tk.Event): The event.
        """
        if sys.platform.startswith("linux"):
            self._parent_canvas.bind_all("<Button-4>", self._on_mouse_wheel, add="+")
            self._parent_canvas.bind_all("<Button-5>", self._on_mouse_wheel, add="+")
            self._parent_canvas.bind_all(
                "<Shift-Button-4>", self._on_shift_mouse_wheel, add="+"
            )
            self._parent_canvas.bind_all(
                "<Shift-Button-5>", self._on_shift_mouse_wheel, add="+"
            )
        else:
            self._parent_canvas.bind_all("<MouseWheel>", self._on_mouse_wheel, add="+")
            self._parent_canvas.bind_all(
                "<Shift-MouseWheel>", self._on_shift_mouse_wheel, add="+"
            )

    def _leave_frame(self, _event: tk.Event) -> None:
        """
        Unbind scrolling events when leaving the frame.

        Parameters:
            _event (tk.Event): The leave event.
        """
        if sys.platform.startswith("linux"):
            self._parent_canvas.unbind_all("<Button-4>")
            self._parent_canvas.unbind_all("<Button-5>")
            self._parent_canvas.unbind_all("<Shift-Button-4>")
            self._parent_canvas.unbind_all("<Shift-Button-5>")
        else:
            self._parent_canvas.unbind_all("<MouseWheel>")
            self._parent_canvas.unbind_all("<Shift-MouseWheel>")


class _DocumentDisplay(DynamicScrollableFrame):
    """Class to display file pages"""

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the Document Editor.

        Args:
            *args: Variable length argument list.
            **kwargs: Configuration arguments for DynamicScrollableFrame.
        """
        super().__init__(*args, **kwargs, orientation="vertical")
        self._images: list[Image] = []
        self._ctk_images: list[ctk.CTkImage] = []
        self._labels: list[ctk.CTkLabel] = []
        self.selected_pages: set[int] = set()
        self._last_selected = 0
        self._rows = 0
        self._columns = 0
        self.scale = 1.0

    @staticmethod
    def _convert_page(page: fitz.Page) -> Image:
        """
        Convert a PyMuPDF page to a PIL.Image.

        Parameters:
            page (fitz.Page): The PyMuPDF page to convert.

        Returns:
            Image: The PIL.Image representation of the page.
        """
        pix = page.get_pixmap()
        mode = "RGBA" if pix.alpha else "RGB"
        img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)

        return img

    def _create_images(
        self, images: list[Image], size: tuple[int, int]
    ) -> list[ctk.CTkImage]:
        """
        Create a list of ctk.CTkImage objects from a list of PIL.Image objects.

        Parameters:
            images (list[Image]): The list of PIL.Image objects to be converted.
            size (tuple[int, int]): The target size of the images.

        Returns:
            list[ctk.CTkImage]: A list of ctk.CTkImage objects created from the input images.
        """
        img_list = []

        for img in images:
            ctk_img = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=(int(size[0] * self.scale), int(size[1] * self.scale)),
            )
            img_list.append(ctk_img)

        return img_list

    def _get_img_size(self, img: Image) -> tuple[int, int]:
        """
        Calculate the size of the image to fit within the canvas while preserving its aspect ratio.

        Parameters:
            img (Image): The image to be resized.

        Returns:
            tuple[int, int]: A tuple containing the width and height of the resized image.
        """
        # Update the canvas to get the current dimensions
        self._parent_canvas.update()

        # Calculate the aspect ratio of the image and canvas
        img_ratio = img.size[0] / img.size[1]
        canvas_width = self._parent_canvas.winfo_width()
        canvas_height = self._parent_canvas.winfo_height()

        if (
            canvas_width - 2 * (PAGE_X_PADDING + PAGE_IPADDING)
        ) / img_ratio <= canvas_height:
            # The image fits within the canvas width
            img_width = canvas_width - 2 * (PAGE_X_PADDING + PAGE_IPADDING)
            img_height = img_width / img_ratio
        else:
            # The image fits within the canvas height
            img_height = canvas_height - 2 * (PAGE_Y_PADDING + PAGE_IPADDING)
            img_width = canvas_height * img_ratio

        return int(img_width), int(img_height)

    def _create_label(self, image: ctk.CTkImage) -> ctk.CTkLabel:
        """Create a CTkLabel for a given CTkImage along corresponding bindings."""
        label = ctk.CTkLabel(self, image=image, text="")
        label.bind("<Button-1>", command=self._select_page)
        label.bind("<Control-Button-1>", command=self._select_pages_control)
        label.bind("<Shift-Button-1>", command=self._select_pages_shift)
        return label

    def _update_grid(self) -> None:
        """Update the grid layout and labels based on the images."""
        columns, _ = self._get_grid_dimension(self._ctk_images[0])
        self._columns = max(1, columns)
        self._rows = max(len(self._images) // self._columns, 1)

        self.update()
        self.rowconfigure(tuple(range(self._columns)), weight=1)
        self.columnconfigure(tuple(range(self._rows)), weight=1)

        for index, label in enumerate(self._labels):
            label.grid(
                column=index % self._columns,
                row=index // self._columns,
                ipadx=PAGE_IPADDING,
                ipady=PAGE_IPADDING,
                padx=PAGE_X_PADDING,
                pady=(0, PAGE_Y_PADDING),
            )
        self.update_idletasks()

        self._parent_canvas.configure(scrollregion=self._parent_canvas.bbox("all"))

    def _get_grid_dimension(self, img: ctk.CTkImage) -> tuple[int, int]:
        """
        Get the grid dimensions based on the parent canvas size.

        Args:
            img (ctk.CTkImage): The image object.

        Returns:
            tuple[int, int]: The grid dimensions.
        """
        self._parent_canvas.update()
        return (
            self._parent_canvas.winfo_width() // img.cget("size")[0],
            self._parent_canvas.winfo_height() // img.cget("size")[1],
        )

    def _update_pages_in_sight(self, document: fitz.Document) -> None:
        """
        Update the visible pages based on the current canvas size and document content.

        Args:
            document (fitz.Document): The document whose pages are being displayed.
        """
        page_in_sight = (
            math.ceil(
                self._parent_canvas.winfo_height()
                / self.winfo_children()[0].winfo_height()
            )
            * self._columns
        )

        self._images[:page_in_sight] = [self._convert_page(page) for page in document]

        self._ctk_images[:page_in_sight] = self._create_images(
            self._images[:page_in_sight], self._get_img_size(self._images[0])
        )
        for index, label in enumerate(self._labels[:page_in_sight]):
            label.configure(image=self._ctk_images[index])

    def _select_page(self, event: tk.Event) -> None:
        """Select page with a single click."""
        self.clear_selection()

        ctk_label: ctk.CTkLabel = event.widget.master

        ctk_label.configure(fg_color=COLOR_SELECTED_BLUE)

        row_num = ctk_label.winfo_y() // ctk_label.winfo_height()
        column_num = ctk_label.winfo_x() // ctk_label.winfo_width()
        page_num = row_num * self._columns + column_num

        self._last_selected = page_num
        self.selected_pages.add(page_num)

    def _select_pages_control(self, event: tk.Event) -> None:
        """Select multiple pages by holding control."""
        ctk_label: ctk.CTkLabel = event.widget.master

        row_num = ctk_label.winfo_y() // ctk_label.winfo_height()
        column_num = ctk_label.winfo_x() // ctk_label.winfo_width()
        page_num = row_num * self._columns + column_num

        if page_num in self.selected_pages:
            self._last_selected = 0
            self.selected_pages.discard(page_num)
            ctk_label.configure(fg_color=ctk_label.cget("bg_color"))
        else:
            self._last_selected = page_num
            self.selected_pages.add(page_num)
            ctk_label.configure(fg_color=COLOR_SELECTED_BLUE)

    def _select_pages_shift(self, event: tk.Event) -> None:
        """Selection a range of pages by holding shift and clicking start and end."""
        ctk_label: ctk.CTkLabel = event.widget.master

        row_num = ctk_label.winfo_y() // ctk_label.winfo_height()
        column_num = ctk_label.winfo_x() // ctk_label.winfo_width()
        page_num = row_num * self._columns + column_num

        if self._last_selected < page_num + 1:
            for label in self._labels[self._last_selected : page_num + 1]:
                label.configure(fg_color=COLOR_SELECTED_BLUE)
        else:
            for label in self._labels[page_num : self._last_selected]:
                label.configure(fg_color=COLOR_SELECTED_BLUE)

        self.selected_pages.update(set(range(self._last_selected, page_num + 1)))

        print(self.selected_pages)

    def clear_selection(self) -> None:
        """Remove selected pages from selection and reset page background."""
        for widget in self.winfo_children():
            widget.configure(fg_color=widget.cget("bg_color"))
        self._last_selected = 0
        self.selected_pages.clear()

    def clear(self) -> None:
        """Remove all widgets within the frame and reset data."""
        for widget in self.winfo_children():
            widget.destroy()

        self._images.clear()
        self._ctk_images.clear()
        self._labels.clear()
        self._rows = 0
        self._columns = 0

        self.update_idletasks()


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

    ctk.CTkLabel(collapsable_frame, text="Test Label").pack(fill="x", expand=True)
    ctk.CTkButton(collapsable_frame, text="Test Button").pack(fill="x", expand=True)

    # debugging scrollable frame
    scrollable_frame = DynamicScrollableFrame(window)  # , orientation="auto")
    scrollable_frame.pack(side="left", expand=True, fill="both")
    # scrollable_frame.grid(column=1, row=0, sticky="news")

    for i in range(50):
        tmp = ctk.CTkLabel(scrollable_frame, text=f"text {i}")
        tmp.pack(fill="x", expand=True)
        # tmp.pack(side="left", fill="y", expand=True)

    window.mainloop()
