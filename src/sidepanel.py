# -*- coding: utf-8 -*-
import math
import tkinter as tk
from typing import Any

import customtkinter as ctk
import fitz  # PyMuPDF
from PIL import Image
from settings import PAGE_X_PADDING
from widgets import CollapsableFrame, DynamicScrollableFrame


class SidePanel(CollapsableFrame):
    """Side panel to preview the file and the selection"""

    def __init__(self, parent: Any):
        """
        Initialize the Side Panel.

        Args:
            parent (Any): The parent widget.
        """
        super().__init__(parent=parent, alignment="left", fg_color="transparent")

        # tabview
        self.tabview = ctk.CTkTabview(master=self, width=253)
        self.tabview.add("Navigator")
        self.tabview.add("Clipboard")
        self.tabview.pack(expand=True, fill="both")

        # preview and navigator tab
        self.navigator_tab = _NavigatorPanel(
            parent=self.tabview.tab("Navigator"))
        self.navigator_tab.pack(expand=True, fill="both")

    def get_new_document(self, document: fitz.Document) -> None:
        """
        Load a new PDF document in the Side Panel.

        Args:
            document (fitz.Document): The PDF document to load.
        """
        self.navigator_tab.get_new_document(document)

    def close_document(self) -> None:
        """Close the current document in the Side Panel."""
        self.navigator_tab.close_document()


class _NavigatorPanel(ctk.CTkFrame):
    """Class to preview document and navigator for the main editor"""

    def __init__(self, parent: Any) -> None:
        """
        Initialize the Navigator Panel.

        Args:
            parent (Any): The parent widget.
        """
        super().__init__(master=parent, fg_color="transparent")

        # data
        self.document = fitz.Document()

        # page view
        self.document_view = _PageView(self, fg_color="transparent", width=210)

    def get_new_document(self, document: fitz.Document) -> None:
        """
        Load a new PDF document.

        Args:
            document (fitz.Document): The PDF document to load.
        """
        self.document = document

        # place page view widget
        self.document_view.pack(expand=True, fill="both")

        self.document_view.load_pages(self.document)

    def close_document(self) -> None:
        """Close the current document."""
        self.document = None

        self.document_view.clear()

        # remove page view widget
        self.document_view.pack_forget()


class _PageView(DynamicScrollableFrame):
    """Preview class to display file pages"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, orientation="vertical")

        # data
        self._labels: list[ctk.CTkLabel] = []

    def load_pages(self, document: fitz.Document) -> None:
        """
        Load and display the pages of a document.

        Parameters:
            document (fitz.Document): The document to load the pages from.
        """
        self.clear()

        for page in document:
            # Convert the page to an image
            image = self._convert_page(page)

            # Create a labeled image widget and pack it
            label = ctk.CTkLabel(self, image=image, text="")
            label.bind("<Button-1>", command=self._select_page)
            label.pack(expand=True, fill="x", padx=PAGE_X_PADDING, pady=7)

            self._labels.append(label)

        self.update_idletasks()
        self._parent_canvas.configure(
            scrollregion=self._parent_canvas.bbox("all"))
        self.update()

        # updates the first few pages so the scrollbar wound overlaps with the images
        if self.winfo_height() > self._parent_canvas.winfo_height():
            self._update_pages_in_sight(document)

    def _convert_page(self, page: fitz.Page) -> ctk.CTkImage:
        """
        Convert a given page object to a displayable Image.

        Args:
            page (fitz.Page): The page to convert to a CTkImage.

        Returns:
            ctk.CTkImage: The converted image.
        """
        pix = page.get_pixmap()
        mode = "RGBA" if pix.alpha else "RGB"
        img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)

        self._parent_canvas.update()

        ratio = img.size[0] / img.size[1]
        img_width = self.winfo_width() - 2 * PAGE_X_PADDING  # - SCROLLBAR_WIDTH

        img_height = img_width / ratio

        ctk_img = ctk.CTkImage(
            light_image=img, dark_image=img, size=(
                int(img_width), int(img_height))
        )

        return ctk_img

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

        for index in range(page_in_sight):
            img = self._convert_page(document[index])
            self._labels[index].configure(image=img)

    def _select_page(self, event: tk.Event) -> None:
        """Select q page with a single click and jumps to it in the main editor."""

    def clear(self) -> None:
        """Clear all child widgets from the container."""
        for widget in self.winfo_children():
            widget.destroy()

        self._labels.clear()

        self.update_idletasks()
