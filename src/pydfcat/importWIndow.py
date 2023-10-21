# -*- coding: utf-8 -*-
from typing import Any, Callable

import customtkinter as ctk
import fitz  # PyMuPDF
from PIL import Image

from .settings import (
    COLOR_SELECTED_BLUE,
    IMPORT_WINDOW_HEIGHT_RATIO,
    PAGE_IPADDING,
    PAGE_X_PADDING,
    TOOLBAR_HEIGHT,
    TOOLBAR_WIDGET_BORDER_SPACING,
    TOOLBAR_WIDGET_HEIGHT,
    TOOLBAR_X_PADDING,
    TOOLBAR_Y_PADDING,
)
from .widgets import _DocumentDisplay


class ImportWindow(ctk.CTkToplevel):
    def __init__(self, parent: Any, proceed_command: Callable, on_closing: Callable):
        super().__init__(master=parent)

        # data
        self.document = fitz.Document()
        self.proceed_command = proceed_command
        self.on_closing = on_closing

        # window properties
        height = int(self.winfo_screenheight() / IMPORT_WINDOW_HEIGHT_RATIO)
        width = height

        # configure window
        self.title("Select the pages you want to import")
        self.geometry(f"{width}x{height}")

        # page view
        self.page_view = _DocumentPreview(self)
        self.page_view.pack(expand=True, fill="both")

        # ui frame
        self.ui_frame = ctk.CTkFrame(self, height=TOOLBAR_HEIGHT)
        self.ui_frame.pack(expand=False, fill="x")

        # buttons
        ok_button = ctk.CTkButton(
            self.ui_frame,
            text="ok",
            height=TOOLBAR_WIDGET_HEIGHT,
            border_spacing=TOOLBAR_WIDGET_BORDER_SPACING,
            command=self.proceed,
        )
        ok_button.pack(
            side="right",
            fill="both",
            expand=True,
            padx=TOOLBAR_X_PADDING,
            pady=TOOLBAR_Y_PADDING,
        )

        # events
        self.protocol("WM_DELETE_WINDOW", self.close)

    def load_pages(self, document: fitz.Document) -> None:
        self.document = document
        self.page_view.load_pages(document)

        # events
        self.bind("<Configure>", lambda _: self.page_view.update_view())

    def proceed(self):
        selection = sorted(self.page_view.selected_pages)
        self.document.select(selection)
        self.proceed_command(self.document)
        self.destroy()

    def close(self):
        self.on_closing()
        self.destroy()


class _DocumentPreview(_DocumentDisplay):
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
            label = self._create_label(image)
            label.configure(fg_color=COLOR_SELECTED_BLUE)
            self._labels.append(label)

        self.selected_pages = set(range(0, len(document)))
        self._last_selected = len(document) - 1

        self._update_grid()

        # updates the first few pages so the scrollbar wound overlaps with the images
        if self.winfo_height() > self._parent_canvas.winfo_height():
            self._update_pages_in_sight(document)

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

        rows = canvas_width // (
            int(self.winfo_screenheight() / IMPORT_WINDOW_HEIGHT_RATIO) / 3
        )
        img_width = canvas_width / rows - 2 * (PAGE_X_PADDING + PAGE_IPADDING)
        img_height = img_width / img_ratio

        return int(img_width), int(img_height)

    def update_view(self) -> None:
        # new_size = self._get_img_size(self._images[0])
        #
        # if new_size and self._ctk_images[0].cget("size") != new_size:
        #     self._ctk_images = self._create_images(self._images, new_size)
        #     for label, img in zip(self._labels, self._ctk_images):
        #         label.configure(image=img)

        columns, _ = self._get_grid_dimension(self._ctk_images[0])

        if not columns == self._columns:
            self._update_grid()


def __load_test_doc(window: ImportWindow, path: str):
    doc = fitz.Document(path)

    window.load_pages(doc)


if __name__ == "__main__":
    root = ctk.CTk()

    window = ImportWindow(root, print, lambda: print("closing"))
    window.after(
        1000,
        lambda: __load_test_doc(
            window,
            "/home/sebastian/Programming/20_Python/21_Projects/PDFCat/test_pdfs/"
            "20210830 10. Hygieneplan ohne Markierung der Änderungen.pdf",
        ),
    )

    root.mainloop()
