# -*- coding: utf-8 -*-
import math
import re
import tkinter as tk
from typing import Any, Callable, Optional

import customtkinter as ctk
import fitz  # PyMuPDF
from CTkMessagebox import CTkMessagebox
from PIL import Image
from settings import (
    COLOR_MAIN_EDITOR_BACKGROUND,
    COLOR_SELECTED_BLUE,
    PAGE_IPADDING,
    PAGE_X_PADDING,
    PAGE_Y_PADDING,
)
from widgets import DynamicScrollableFrame


class MainEditor(ctk.CTkFrame):
    """Main editor class to manage file pages"""

    def __init__(
        self, parent: Any, open_file_command: Callable, scaling_variable: ctk.StringVar
    ) -> None:
        """
        Initialize the Main Editor.

        Args:
            parent (Any): The parent widget.
            open_file_command (Callable): The command to open a file.
        """
        super().__init__(master=parent, fg_color="transparent")

        # data
        self.document = fitz.Document()
        self.scaling_variable = scaling_variable

        # ui frame
        self.ui_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.ui_frame.pack(expand=True, fill="both")
        self.ui_frame.rowconfigure((0, 1), weight=1, uniform="a")
        self.ui_frame.columnconfigure(0, weight=1)

        # button to open file
        self.open_file_button = ctk.CTkButton(
            self.ui_frame, text="open file", command=open_file_command
        )

        self.open_file_button.grid(row=0, column=0, sticky="s", pady=5)

        # page view
        self.document_view = _DocumentEditor(self, fg_color="transparent")

        # label for error message
        self.error_label = ctk.CTkLabel(
            self.ui_frame, text="Wrong file type!", text_color="#FF0000"
        )

    def get_new_document(self, document: fitz.Document) -> None:
        """
        Load a new document into the Main Editor.

        Args:
            document (fitz.Document): The document to load.
        """
        self.document = document

        # remove file-open-button and place page view
        self.ui_frame.pack_forget()
        self.error_label.grid_forget()
        self.document_view.pack(expand=True, fill="both")

        self.document_view.load_pages(self.document)

        # events
        self.bind("<Configure>", self.update_document)

    def update_document(self, _event: tk.Event) -> None:
        """
        Update the document in response to a resize event.

        Args:
            _event (tk.Event): The event object.
        """
        self.document_view.update_pages()

    def update_scaling(self, scale_string: str) -> None:
        """
        Update the scaling factor of the document view.

        Parameters:
            scale_string (str): The scaling factor as a percentage.
        """
        # Check if the scale string matches the expected format
        if not re.match(r"^([1-9]([0-9]){1,2})%$", scale_string):
            # Show an error message if the scale string is invalid
            CTkMessagebox(
                title="Invalid scaling",
                icon="warning",
                message="You entered an invalid scaling factor. "
                "Please make sure you entered a number.",
            )
            self.scaling_variable.set("100%")
            return

        scale = scale_string[:-1]

        # Check if the scale is greater than 200%
        if int(scale) > 200:
            # Show an error message if the scale is too high
            CTkMessagebox(
                title="Invalid scaling",
                icon="warning",
                message="You entered a too high scaling. "
                "Please enter a scaling smaller than 200%.",
            )
            self.scaling_variable.set("100%")
            return

        # Convert the scale to a decimal value
        scale_decimal = int(scale) / 100

        # Update the scaling of the document view
        self.document_view.update_pages(scale_decimal)

    def open_file_error(self) -> None:
        """display error message"""
        if not self.document_view.winfo_ismapped():
            self.error_label.grid(row=1, column=0, sticky="n", pady=5)

    def jump_to_page(self, page_num: int) -> None:
        self.document_view.jump_to_page(page_num)

    def close_document(self) -> None:
        """Close the current document in the Main Editor."""
        self.document = None

        self.document_view.clear()

        # remove page view and place file-open-button
        self.document_view.pack_forget()
        self.error_label.grid_forget()
        self.ui_frame.pack(expand=True, fill="both")

        # events
        self.unbind("<Configure>")


class _DocumentEditor(DynamicScrollableFrame):
    """Class to display file pages"""

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the Document Editor.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs, orientation="vertical")
        self._images: list[Image] = []
        self._ctk_images: list[ctk.CTkImage] = []
        self._labels: list[ctk.CTkLabel] = []
        self._selected_pages: set[int] = set()
        self._last_selected = 0
        self._rows = 0
        self._columns = 0
        self._scale = 1.0

    def load_pages(self, document: fitz.Document) -> None:
        """
        Display the document pages by creating new labels.

        Args:
            document (fitz.Document): The document to display.
        """
        self.clear()
        self._images = [self._convert_page(page) for page in document]
        self._ctk_images = self._create_images(
            self._images, self._get_img_size(self._images[0])
        )
        for image in self._ctk_images:
            label = ctk.CTkLabel(self, image=image, text="")
            label.bind("<Button-1>", command=self._select_page)
            label.bind("<Control-Button-1>",
                       command=self._select_pages_control)
            label.bind("<Shift-Button-1>", command=self._select_pages_shift)
            self._labels.append(label)

        self._update_grid()

        # updates the first few pages so the scrollbar wound overlaps with the images
        if self.winfo_height() > self._parent_canvas.winfo_height():
            self._update_pages_in_sight(document)

    def update_pages(self, new_scaling: Optional[float] = None) -> None:
        """
        Update the document pages with a new scaling factor or new image size.

        Parameters:
            new_scaling (float, optional): The new scaling factor for the images.
        """
        new_size = self._get_img_size(self._images[0])

        if new_scaling is not None:
            self._scale = new_scaling

        if new_scaling is not None or (
            new_size and self._ctk_images[0].cget("size") != new_size
        ):
            self._ctk_images = self._create_images(self._images, new_size)
            for label, img in zip(self._labels, self._ctk_images):
                label.configure(image=img)

        self._update_grid()

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
                size=(int(size[0] * self._scale), int(size[1] * self._scale)),
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

        if (canvas_width - 2 * PAGE_X_PADDING) / img_ratio <= canvas_height:
            # The image fits within the canvas width
            img_width = canvas_width - 2 * PAGE_X_PADDING
            img_height = canvas_width / img_ratio
        else:
            # The image fits within the canvas height
            img_height = canvas_height
            img_width = canvas_height * img_ratio

        return int(img_width), int(img_height)

    def _update_grid(self) -> bool:
        """
        Update the grid layout and labels based on the images.

        Returns:
            bool: True if the grid layout was updated, False otherwise.
        """
        columns, rows = self._get_grid_dimension(self._ctk_images[0])

        if columns == self._columns:
            return False

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

        self._parent_canvas.configure(
            scrollregion=self._parent_canvas.bbox("all"))

        return True

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
        page_in_sight = math.ceil(
            self._parent_canvas.winfo_height(
            ) / self.winfo_children()[0].winfo_height()
        )

        self._images[:page_in_sight] = [
            self._convert_page(page) for page in document]

        self._ctk_images[:page_in_sight] = self._create_images(
            self._images[:page_in_sight], self._get_img_size(self._images[0])
        )
        for index, label in enumerate(self._labels[:page_in_sight]):
            label.configure(image=self._ctk_images[index])

    def jump_to_page(self, page_num: int) -> None:
        page_overlap = 1 if len(self._labels) % self._columns != 0 else 0
        row_num = page_num // self._columns

        self._parent_canvas.yview_moveto(
            str(row_num / (self._rows + page_overlap)))

    def _select_page(self, event: tk.Event) -> None:
        """Select page with a single click."""
        self.clear_selection()

        ctk_label: ctk.CTkLabel = event.widget.master

        ctk_label.configure(fg_color=COLOR_SELECTED_BLUE)

        row_num = ctk_label.winfo_y() // ctk_label.winfo_height()
        column_num = ctk_label.winfo_x() // ctk_label.winfo_width()
        page_num = row_num * self._columns + column_num

        self._last_selected = page_num
        self._selected_pages.add(page_num)

    def _select_pages_control(self, event: tk.Event) -> None:
        """Select multiple pages by holding control."""
        ctk_label: ctk.CTkLabel = event.widget.master

        row_num = ctk_label.winfo_y() // ctk_label.winfo_height()
        column_num = ctk_label.winfo_x() // ctk_label.winfo_width()
        page_num = row_num * self._columns + column_num

        if page_num in self._selected_pages:
            self._last_selected = 0
            self._selected_pages.discard(page_num)
            ctk_label.configure(fg_color=COLOR_MAIN_EDITOR_BACKGROUND)
        else:
            self._last_selected = page_num
            self._selected_pages.add(page_num)
            ctk_label.configure(fg_color=COLOR_SELECTED_BLUE)

    def _select_pages_shift(self, event: tk.Event) -> None:
        """Selection a range of pages by holding shift and clicking start and end."""
        ctk_label: ctk.CTkLabel = event.widget.master

        row_num = ctk_label.winfo_y() // ctk_label.winfo_height()
        column_num = ctk_label.winfo_x() // ctk_label.winfo_width()
        page_num = row_num * self._columns + column_num

        if self._last_selected < page_num + 1:
            for label in self.winfo_children()[self._last_selected: page_num + 1]:
                label.configure(fg_color=COLOR_SELECTED_BLUE)
        else:
            for label in self.winfo_children()[page_num: self._last_selected]:
                label.configure(fg_color=COLOR_SELECTED_BLUE)

        self._selected_pages.update(
            {page_index for page_index in range(
                self._last_selected, page_num + 1)}
        )

    def clear_selection(self) -> None:
        """Remove selected pages from selection and reset page background."""
        for widget in self.winfo_children():
            widget.configure(fg_color=COLOR_MAIN_EDITOR_BACKGROUND)
        self._last_selected = 0
        self._selected_pages.clear()

    def clear(self) -> None:
        """Remove all widgets within the frame and reset data."""
        for widget in self.winfo_children():
            widget.destroy()

        self._images.clear()
        self._ctk_images.clear()
        self._labels.clear()
        self._rows = 0

        self.update_idletasks()
