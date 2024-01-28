# -*- coding: utf-8 -*-
import re
import tkinter as tk
from typing import Any, Callable, Optional

import customtkinter as ctk
import fitz  # PyMuPDF
from CTkMessagebox import CTkMessagebox

from .journal import DocumentJournal
from .loadingWindow import LoadingWindow
from .settings import COLOR_SELECTED_BLUE
from .widgets import _DocumentDisplay


class MainEditor(ctk.CTkFrame):
    """Main editor class to manage file pages."""

    def __init__(
        self,
        parent: Any,
        open_file_command: Callable,
        scaling_variable: ctk.StringVar,
    ) -> None:
        """
        Initialize the Main Editor.

        Args:
            parent (Any): The parent widget.
            open_file_command (Callable): The command to open a file.
        """
        super().__init__(master=parent, fg_color="transparent")

        # data
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

    def get_new_document(
        self, document: fitz.Document, loading_window: LoadingWindow
    ) -> None:
        """
        Load a new document into the Main Editor.

        Args:
            document (fitz.Document): The document to load.
            loading_window (LoadingWindow): A window with loadingbar.
        """
        # remove file-open-button and place page view
        self.ui_frame.pack_forget()
        self.error_label.grid_forget()
        self.document_view.pack(expand=True, fill="both")

        self.document_view.load_pages(document, loading_window)

        # events
        self.bind("<Configure>", lambda _: self.document_view.update_pages())

    def update_scaling(self, scale_string: str) -> None:
        """
        Update the scaling factor of the document view.

        Parameters:
            scale_string (str): The scaling factor as a percentage.
        """
        if re.match(r"^[0-9]+%$", scale_string):
            scale_number_string = scale_string[:-1]
        else:
            scale_number_string = scale_string
            self.scaling_variable.set(f"{scale_number_string}%")
        try:
            scale = int(scale_number_string)
        except ValueError:
            # Show an error message if the scale isn't a hole number
            CTkMessagebox(
                title="Invalid scaling (invalid input)",
                icon="warning",
                message="You entered an invalid scaling factor. "
                "Please make sure you entered a hole number.",
            )
            self.scaling_variable.set(f"{self.document_view.scale * 100:.0f}%")
            return

        # Check if the scale is less than 10%
        if scale < 10:
            # Show an error message if the scale is too low
            CTkMessagebox(
                title="Invalid scaling (to low)",
                icon="warning",
                message="You entered a too low scaling. "
                "Please enter a scaling bigger then or equal to 10%.",
            )
            self.scaling_variable.set(f"{self.document_view.scale * 100:.0f}%")

        # Check if the scale is greater than 200%
        elif scale > 200:
            # Show an error message if the scale is too high
            CTkMessagebox(
                title="Invalid scaling (to high)",
                icon="warning",
                message="You entered a too high scaling. "
                "Please enter a scaling smaller than 200%.",
            )
            self.scaling_variable.set(f"{self.document_view.scale * 100:.0f}%")

        else:
            # Convert the scale to a decimal value
            scale_decimal = scale / 100
            # Update the scaling of the document view
            self.document_view.update_pages(scale_decimal)

    def open_file_error(self) -> None:
        """Display error message."""
        if not self.document_view.winfo_ismapped():
            self.error_label.grid(row=1, column=0, sticky="n", pady=5)

    def jump_to_page(self, page_num: int) -> None:
        """
        Jump in the main editor to the specified page number.

        Args:
            page_num (int): The page number to jump to.
        """
        self.document_view.jump_to_page(page_num)

    def get_selection(self) -> set[int]:
        """
        Get the selected pages from the document view.

        Returns:
            set[int]: A set of selected page numbers.
        """
        return self.document_view.selected_pages

    def delete_pages(self, page_numbers: list[int]) -> None:
        """
        Delete specific pages from the document view.

        Args:
            page_numbers (list[int]): The page numbers to delete.
        """
        self.document_view.delete_pages(page_numbers)

    def duplicate_pages(self, page_numbers: list[int]) -> None:
        """
        Duplicate specific pages in the document view.

        Args:
            page_numbers (list[int]): The page numbers to duplicate.
        """
        self.document_view.duplicate_pages(page_numbers)

    def insert_pages(self, position: int, pages: fitz.Document) -> None:
        """
        Insert pages from another document at a given position in the document view.

        Args:
            position (int): The position to insert the pages.
            pages (fitz.Document): The pages to be inserted.
        """
        self.document_view.insert_pages(position, pages)

    def select_range(self, start: int, end: int) -> None:
        """
        Select a range of pages in the document view.

        Args:
            start (int): The start page number of the selection.
            end (int): The end page number of the selection.
        """
        self.document_view.set_selection(range(start, end))

    def clear_selection(self) -> None:
        """Clear the current selection in the document view."""
        self.document_view.clear_selection()

    def close_document(self) -> None:
        """Close the current document in the Main Editor."""
        self.document_view.clear()

        # remove page view and place file-open-button
        self.document_view.pack_forget()
        self.error_label.grid_forget()
        self.ui_frame.pack(expand=True, fill="both")

        # events
        self.unbind("<Configure>")


class _DocumentEditor(_DocumentDisplay):
    """Class to display file pages"""

    journal: DocumentJournal

    def load_pages(
        self, document: fitz.Document, loading_window: LoadingWindow
    ) -> None:
        """
        Display the document pages by creating new labels.

        Args:
            document (fitz.Document): The document to display.
            loading_window (LoadingWindow): Window for loading animation.
        """
        loading_window.aim(percentage=0.5, absolut=len(document) + 2)

        self.clear()
        self._images = [self._convert_page(page) for page in document]
        self._ctk_images = self._create_images(
            self._images, self._get_img_size(self._images[0])
        )

        loading_window.add()

        for image in self._ctk_images:
            label = self._create_label(image)
            self._labels.append(label)

            loading_window.add()

        self._update_grid()

        loading_window.add()

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
            self.scale = new_scaling

        if new_scaling is not None or (
            new_size and self._ctk_images[0].cget("size") != new_size
        ):
            self._ctk_images = self._create_images(self._images, new_size)
            for label, img in zip(self._labels, self._ctk_images):
                label.configure(image=img)

        columns, _ = self._get_grid_dimension(self._ctk_images[0])

        if not columns == self._columns:
            self._update_grid()

    def jump_to_page(self, page_num: int) -> None:
        """
        Jump to the specified page number.

        Args:
            page_num (int): The page number to jump to.
        """
        page_overlap = 1 if len(self._labels) % self._columns != 0 else 0
        row_num = page_num // self._columns

        self._parent_canvas.yview_moveto(str(row_num / (self._rows + page_overlap)))

    def delete_pages(self, page_nums: list[int]) -> None:
        """
        Delete specific pages from the view.

        Args:
            page_nums (list[int]): The page numbers to delete.
        """
        for n, page_num in enumerate(page_nums):
            self._labels.pop(page_num - n).grid_forget()
            self._images.pop(page_num - n)
            self._ctk_images.pop(page_num - n)

        self._update_grid()

    def duplicate_pages(self, page_nums: list[int]) -> None:
        """
        Duplicate specific pages in the view.

        Args:
            page_nums (list[int]): The page numbers to duplicate.
        """
        position = max(page_nums) + 1
        for n, page_num in enumerate(page_nums):
            self._images.insert(position + n, self._images[page_num])
            self._ctk_images.insert(position + n, self._ctk_images[page_num])

            label = self._create_label(self._labels[page_num].cget("image"))
            self._labels.insert(position + n, label)

        self._update_grid()

    def insert_pages(self, pos: int, pages: fitz.Document) -> None:
        """
        Insert pages from another document at a given position in the view.

        Args:
            pos (int): The position to insert the pages.
            pages (fitz.Document): The pages to be inserted.
        """
        self._images[pos:pos] = [self._convert_page(page) for page in pages]
        self._ctk_images[pos:pos] = self._create_images(
            self._images[pos : pos + len(pages)],
            self._get_img_size(self._images[0]),
        )

        for n, image in enumerate(self._ctk_images[pos : pos + len(pages)]):
            label = self._create_label(image)
            self._labels.insert(pos + n, label)

        self._update_grid()

    def _select_page(self, event: tk.Event) -> None:
        super()._select_page(event)
        self.journal.main.change_selection(sorted(self.selected_pages))

    def _select_pages_control(self, event: tk.Event) -> None:
        super()._select_pages_control(event)
        self.journal.main.change_selection(sorted(self.selected_pages))

    def _select_pages_shift(self, event: tk.Event) -> None:
        super()._select_pages_shift(event)
        self.journal.main.change_selection(sorted(self.selected_pages))

    def set_selection(self, index_range: range) -> None:
        """Select a given range of pages in the main editor."""
        self.clear_selection()

        selected_page = 0
        for selected_page in index_range:
            self._labels[selected_page].configure(fg_color=COLOR_SELECTED_BLUE)
            self.selected_pages.add(selected_page)

        self._last_selected = selected_page
