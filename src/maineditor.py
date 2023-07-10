# -*- coding: utf-8 -*-
import tkinter as tk
from typing import Any, Callable

import customtkinter as ctk
import fitz  # PyMuPDF
from PIL import Image


class MainEditor(ctk.CTkFrame):
    def __init__(self, parent: Any, open_file_command: Callable) -> None:
        """
        Initialize the Main Editor.

        Args:
            parent (Any): The parent widget.
            open_file_command (Callable): The command to open a file.
        """
        super().__init__(master=parent, fg_color="transparent")

        # data
        self.document = fitz.Document()

        # button to open file
        self.open_file_button = ctk.CTkButton(self, text="open file", command=open_file_command)
        self.open_file_button.pack(expand=True)

        # page view
        self.document_view = _DocumentEditor(self, fg_color="transparent", orientation="vertical")

    def get_new_document(self, document: fitz.Document) -> None:
        """
        Load a new document into the Main Editor.

        Args:
            document (fitz.Document): The document to load.
        """
        self.document = document

        # remove file-open-button and place page view
        self.open_file_button.pack_forget()
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
        self.document_view.update_pages(self.document)

    def close_document(self):
        """
        Close the current document in the Main Editor.
        """
        self.document = None

        self.document_view.clear()

        # remove page view and place file-open-button
        self.document_view.pack_forget()
        self.open_file_button.pack(expand=True)

        # events
        self.unbind("<Configure>")


class _DocumentEditor(ctk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the Document Editor.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self._images: list[ctk.CTkImage] = []
        self._labels: list[ctk.CTkLabel] = []
        self._rows = 0

    def load_pages(self, document: fitz.Document) -> None:
        """
        Display the document pages by creating new labels.

        Args:
            document (fitz.Document): The document to display.
        """
        self._images = [self._convert_page(page) for page in document]
        self._labels = [ctk.CTkLabel(self, image=image, text="") for image in self._images]
        self._update_grid()

    def update_pages(self, document: fitz.Document) -> None:
        """
        Update the document pages if there is a change in grid dimensions.

        Args:
            document (fitz.Document): The updated document.
        """
        # self._images = [self._convert_page(page) for page in document]
        self._update_grid()

    def _convert_page(self, page: fitz.Page) -> ctk.CTkImage:
        """
        Convert a given page object to a displayable Image.

        Args:
            page (fitz.Page): The page to convert.

        Returns:
            ctk.CTkImage: The converted image.
        """
        pix = page.get_pixmap()
        mode = "RGBA" if pix.alpha else "RGB"
        img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)

        self._parent_canvas.update()

        ratio = img.size[0] / img.size[1]
        canvas_width = self._parent_canvas.winfo_width()
        canvas_height = self._parent_canvas.winfo_height()

        img_width = canvas_height * ratio if ratio < 1 else canvas_width
        img_height = canvas_height if ratio < 1 else canvas_width / ratio
        if img_height > canvas_height:
            img_height = canvas_height
            img_width = img_height * ratio

        scale = 1

        ctk_img = ctk.CTkImage(
            light_image=img,
            dark_image=img,
            size=(int(img_width * scale), int(img_height * scale))
        )

        return ctk_img

    def _update_grid(self) -> bool:
        """
        Update the grid layout and labels based on the images.

        Returns:
            bool: True if the grid layout was updated, False otherwise.
        """
        rows, _ = self._get_grid_dimension(self._images[0])

        if rows == self._rows:
            return False

        self._rows = max(1, rows)

        self.rowconfigure(tuple(range(self._rows)), weight=1)
        self.columnconfigure(tuple(range(len(self._images) // self._rows)), weight=1)

        for index, label in enumerate(self._labels):
            label.grid(column=index % self._rows, row=index // self._rows, padx=5, pady=7)

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
            self._parent_canvas.winfo_height() // img.cget("size")[1]
        )

    def clear(self) -> None:
        """
        Remove all widgets within the frame and reset data.
        """
        self._images = []
        self._labels = []
        self._rows = 0
        for widget in self.winfo_children():
            widget.destroy()
