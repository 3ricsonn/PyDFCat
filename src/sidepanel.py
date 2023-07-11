# -*- coding: utf-8 -*-
from typing import Any

import customtkinter as ctk
import fitz  # PyMuPDF
from PIL import Image

from widgets import CollapsableFrame


class SidePanel(CollapsableFrame):
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
        """
        Close the current document in the Side Panel.
        """
        self.navigator_tab.close_document()


class _NavigatorPanel(ctk.CTkFrame):
    def __init__(self, parent: Any):
        """
        Initialize the Navigator Panel.

        Args:
            parent (Any): The parent widget.
        """
        super().__init__(master=parent, fg_color="transparent")

        # data
        self.document = fitz.Document()

        # page view
        self.document_view = _PageView(self)

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
        """
        Close the current document.
        """
        self.document = None

        self.document_view.clear()

        # remove page view widget
        self.document_view.pack_forget()


class _PageView(ctk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # data

    def load_pages(self, document: fitz.Document) -> None:
        for page in document:
            image = self._convert_page(page)

            ctk.CTkLabel(self, image=image, text="").pack(
                expand=True, fill="x", padx=5, pady=7)

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
        img_width = self._parent_canvas.winfo_width()
        img_height = img_width / ratio

        ctk_img = ctk.CTkImage(
            light_image=img,
            dark_image=img,
            size=(int(img_width), int(img_height))
        )

        return ctk_img

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()
