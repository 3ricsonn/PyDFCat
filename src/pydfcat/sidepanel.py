# -*- coding: utf-8 -*-
import math
import tkinter as tk
from typing import Any, Callable

import customtkinter as ctk
import fitz  # PyMuPDF
import os
from PIL import Image

from .loadingWindow import LoadingWindow
from .settings import (
    CLIPB_TOOLBAR_IMAGE_HEIGHT,
    CLIPB_TOOLBAR_IMAGE_WIDTH,
    CLIPB_TOOLBAR_PADDING,
    CLIPB_TOOLBAR_WIDGET_BORDER_SPACING,
    CLIPB_TOOLBAR_WIDGET_HEIGHT,
    CLIPB_TOOLBAR_WIDGET_WIDTH,
    COLOR_CLOSE_RED,
    COLOR_SELECTED_BLUE,
    DIRNAME,
    PAGE_IPADDING,
    PAGE_X_PADDING,
    PAGE_Y_PADDING,
)
from .widgets import CollapsableFrame, DynamicScrollableFrame


try:
    from CTkToolTip import CTkToolTip

    tooltip = True
except ModuleNotFoundError:
    tooltip = False


class _PageView(DynamicScrollableFrame):
    def __init__(self, parent, **kwargs) -> None:
        """
        Initialize the _PageView.

        Args:
            parent: The parent widget.
            **kwargs: Configuration arguments for DynamicScrollableFrame.
        """
        super().__init__(master=parent, **kwargs, orientation="vertical")

        # data
        self._labels: list[ctk.CTkLabel] = []

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
        img_width = self._parent_canvas.winfo_width() - 2 * (
            PAGE_IPADDING + PAGE_X_PADDING
        )
        img_height = img_width / ratio

        ctk_img = ctk.CTkImage(
            light_image=img, dark_image=img, size=(int(img_width), int(img_height))
        )

        return ctk_img

    def _create_label(self, image: ctk.CTkImage) -> ctk.CTkLabel:
        label = ctk.CTkLabel(self, image=image, text="")
        label.bind("<Button-1>", command=self._select_page)
        return label

    def _place_label(self):
        for widget in self.winfo_children():
            widget.pack_forget()

        for label in self._labels:
            label.pack(
                expand=True,
                fill="x",
                ipadx=PAGE_IPADDING,
                ipady=PAGE_IPADDING,
                padx=PAGE_X_PADDING,
                pady=(0, PAGE_Y_PADDING),
            )
            self.update()

    def _select_page(self, event: tk.Event) -> None:
        pass


class SidePanel(CollapsableFrame):
    """Side panel to preview the file and the selection."""

    def __init__(self, parent: Any, jump_to_page_command: Callable):
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
        self.navigator = _NavigatorPanel(
            parent=self.tabview.tab("Navigator"),
            jump_to_page_command=jump_to_page_command,
        )
        self.navigator.pack(expand=True, fill="both")

        # clipboard tab
        self.clipboard = _ClipboardPanel(parent=self.tabview.tab("Clipboard"))
        self.clipboard.pack(expand=True, fill="both")

    def get_new_document(
        self, document: fitz.Document, loading_window: LoadingWindow
    ) -> None:
        """
        Load a new PDF document in the Side Panel.

        Args:
            document (fitz.Document): The PDF document to load.
            loading_window (LoadingWindow): Window for loading animation.
        """
        self.tabview.set("Navigator")
        self.navigator.get_new_document(document, loading_window)


class _NavigatorPanel(ctk.CTkFrame):
    """Class to preview document and navigator for the main editor."""

    def __init__(self, parent: Any, jump_to_page_command: Callable) -> None:
        """
        Initialize the Navigator Panel.

        Args:
            parent (Any): The parent widget.
        """
        super().__init__(master=parent, fg_color="transparent")

        # page view
        self.document_view = _NavigatorPageView(self, jump_to_page_command)

    def get_new_document(
        self, document: fitz.Document, loading_window: LoadingWindow
    ) -> None:
        """
        Load a new PDF document.

        Args:
            document (fitz.Document): The PDF document to load.
            loading_window (LoadingWindow): Window for loading animation.
        """
        # place page view widget
        self.document_view.pack(expand=True, fill="both")

        self.document_view.load_pages(document, loading_window)

    def delete_pages(self, page_numbers: list[int]) -> None:
        self.document_view.delete_pages(page_numbers)

    def duplicate_pages(self, page_numbers: list[int]) -> None:
        self.document_view.duplicate_pages(page_numbers)

    def insert_pages(self, position: int, pages: fitz.Document) -> None:
        self.document_view.insert_pages(position, pages)

    def close_document(self) -> None:
        """Close the current document."""
        self.document_view.clear()

        # remove page view widget
        self.document_view.pack_forget()


class _NavigatorPageView(_PageView):
    """
    A class representing a preview to display file pages.

    This class inherits from DynamicScrollableFrame, a custom scrollable frame class.
    """

    def __init__(self, parent, jump_page_command: Callable, **kwargs) -> None:
        """
        Initialize the _NavigatorPageView.

        Args:
            parent: The parent widget.
            jump_page_command (Callable): A callable to jump to a specific page.
            **kwargs: Configuration arguments for DynamicScrollableFrame.
        """
        super().__init__(parent=parent, **kwargs)

        # data
        self._jump_to_page = jump_page_command

    def load_pages(
        self, document: fitz.Document, loading_window: LoadingWindow
    ) -> None:
        """
        Load and display the pages of a document.

        Parameters:
            document (fitz.Document): The document to load the pages from.
            loading_window (LoadingWindow): Window for loading animation.
        """
        loading_window.aim(percentage=0.5, absolut=len(document) + 1)
        self.clear()

        for page in document:
            # Convert the page to an image
            image = self._convert_page(page)

            # Create a labeled image widget and pack it
            label = self._create_label(image)

            self._labels.append(label)

            loading_window.add()

        self._place_label()

        self.update_idletasks()
        self._parent_canvas.configure(scrollregion=self._parent_canvas.bbox("all"))
        self.update()

        loading_window.add()

        # updates the first few pages so the scrollbar wound overlaps with the images
        if self.winfo_height() > self._parent_canvas.winfo_height():
            self._update_pages_in_sight(document)

    def _update_pages_in_sight(self, document: fitz.Document) -> None:
        """
        Update the visible pages based on the current canvas size and document content.

        Args:
            document (fitz.Document): The document whose pages are being displayed.
        """
        page_in_sight = math.ceil(
            self._parent_canvas.winfo_height() / self.winfo_children()[0].winfo_height()
        )

        for index in range(page_in_sight):
            img = self._convert_page(document[index])
            self._labels[index].configure(image=img)

    def _select_page(self, event: tk.Event) -> None:
        """Select a page with a single click and jumps to it in the main editor."""
        self.clear_selection()

        ctk_label: ctk.CTkLabel = event.widget.master

        ctk_label.configure(fg_color=COLOR_SELECTED_BLUE)

        page_num = ctk_label.winfo_y() // ctk_label.winfo_height()

        self._jump_to_page(page_num)

    def delete_pages(self, page_nums: list[int]) -> None:
        for n, page_num in enumerate(page_nums):
            self._labels.pop(page_num - n).pack_forget()

    def duplicate_pages(self, page_nums: list[int]) -> None:
        # TODO: what if page nums aren't continues
        position = max(page_nums) + 1
        for n, page_num in enumerate(page_nums):
            label = self._create_label(self._labels[page_num].cget("image"))
            self._labels.insert(position + n, label)
        self._place_label()

    def insert_pages(self, pos: int, pages: fitz.Document) -> None:
        pass

    def clear_selection(self) -> None:
        """Remove selected pages from selection and reset page background."""
        for widget in self.winfo_children():
            widget.configure(fg_color=widget.cget("bg_color"))

    def clear(self) -> None:
        """Clear all child widgets from the container."""
        for widget in self.winfo_children():
            widget.destroy()

        self._labels.clear()

        self.update_idletasks()


class _ClipboardPanel(ctk.CTkFrame):
    """
    A private class representing a clipboard panel.

    This class inherits from ctk.CTkFrame, a custom Tkinter Frame class.
    It's intended to be used internally within the Clipboard class.
    """

    def __init__(self, parent: Any, **kwargs):
        """
        Initialize the _ClipboardPanel.

        Args:
            parent: The parent widget.
            **kwargs: Configuration arguments for ctk.CTkFrame.
        """
        super().__init__(master=parent, **kwargs, fg_color="transparent")

        # toolbar
        self.toolbar = ctk.CTkFrame(self, fg_color="transparent")
        self.toolbar.pack(fill="x", pady=CLIPB_TOOLBAR_PADDING)

        # open file to clipboard
        self.open_file_button = ClipboardToolBarButton(
            self.toolbar, button_type="open", tooltip_message="open file to clipboard"
        )
        self.open_file_button.pack(
            side="left",
            expand=True,
            padx=CLIPB_TOOLBAR_PADDING,
            pady=CLIPB_TOOLBAR_PADDING,
        )

        # select all
        self.select_all_button = ClipboardToolBarButton(
            self.toolbar, button_type="select-all", tooltip_message="select all"
        )
        self.select_all_button.pack(
            side="left",
            expand=True,
            padx=CLIPB_TOOLBAR_PADDING,
            pady=CLIPB_TOOLBAR_PADDING,
        )

        # clear selection
        self.clear_select_button = ClipboardToolBarButton(
            self.toolbar,
            button_type="clear-select",
            tooltip_message="clear selection",
        )
        self.clear_select_button.pack(
            side="left",
            expand=True,
            padx=CLIPB_TOOLBAR_PADDING,
            pady=CLIPB_TOOLBAR_PADDING,
        )

        # clear file clipboard
        self.clear_clipboard_button = ClipboardToolBarButton(
            self.toolbar,
            button_type="clear",
            tooltip_message="clear clipboard",
            hover_color=COLOR_CLOSE_RED,
        )
        self.clear_clipboard_button.pack(
            side="left",
            expand=True,
            padx=CLIPB_TOOLBAR_PADDING,
            pady=CLIPB_TOOLBAR_PADDING,
        )

        # clipboard page view
        self.page_view = _ClipboardPageView(self)
        self.page_view.pack(expand=True, fill="both")

    def delete_pages(self, page_numbers: list[int]) -> None:
        self.page_view.delete_pages(page_numbers)

    def insert_pages(self, position: int, pages: fitz.Document) -> None:
        self.page_view.insert_pages(position, pages)

    def enable_tools(self):
        """Enable clipboard tools."""
        self.open_file_button.enable()
        self.select_all_button.enable()
        self.clear_select_button.enable()
        self.clear_clipboard_button.enable()

    def disable_tools(self):
        """Disable clipboard tools."""
        self.open_file_button.disable()
        self.select_all_button.disable()
        self.clear_select_button.disable()
        self.clear_clipboard_button.disable()


class _ClipboardPageView(_PageView):
    """
    A private class representing a view for clipboard pages.

    This class inherits from DynamicScrollableFrame, a custom scrollable frame class.
    It's intended to be used internally within the Clipboard class.
    """

    def delete_pages(self, page_nums: list[int]) -> None:
        pass

    def insert_pages(self, pos: int, pages: fitz.Document) -> None:
        for i, page in enumerate(pages):
            label = self._create_label(self._convert_page(page))
            if pos == -1:
                self._labels.append(label)
            else:
                self._labels.insert(pos + i, label)
        self._place_label()


class ClipboardToolBarButton(ctk.CTkButton):
    """
    A custom toolbar button class for clipboard tools.

    This class inherits from ctk.CTkButton, a custom Tkinter Button class.
    """

    def __init__(self, parent: Any, button_type: str, tooltip_message="", **kwargs):
        """
        Initialize the ClipboardToolBarButton.

        Args:
            parent (Any): The parent widget.
            button_type (str): The type of the button.
            tooltip_message (str, optional):
                The tooltip message for the button.
                Default is an empty string.
            **kwargs: Configuration arguments for ctk.CTkButton.
        """
        super().__init__(
            master=parent,
            text="",
            width=CLIPB_TOOLBAR_WIDGET_WIDTH,
            height=CLIPB_TOOLBAR_WIDGET_HEIGHT,
            border_spacing=CLIPB_TOOLBAR_WIDGET_BORDER_SPACING,
            **kwargs,
        )

        self._type = button_type
        if tooltip:
            self.tooltip = CTkToolTip(self, message=tooltip_message)

        self.disable()

    def enable(self):
        """Enable the button."""
        img_outline = Image.open(
            os.path.join(
                DIRNAME,
                f"assets/clipboard_icons/{self._type}/{self._type}-outline.png",
            )
        )
        ctk_img_outline = ctk.CTkImage(
            img_outline,
            img_outline,
            size=(CLIPB_TOOLBAR_IMAGE_WIDTH, CLIPB_TOOLBAR_IMAGE_HEIGHT),
        )
        img_solid = Image.open(
            os.path.join(
                DIRNAME,
                f"assets/clipboard_icons/{self._type}/{self._type}-solid.png",
            )
        )
        ctk_img_solid = ctk.CTkImage(
            img_solid,
            img_solid,
            size=(CLIPB_TOOLBAR_IMAGE_WIDTH, CLIPB_TOOLBAR_IMAGE_HEIGHT),
        )

        self.configure(image=ctk_img_outline, state="normal")
        self.bind("<Enter>", lambda _: self.configure(image=ctk_img_solid), add="+")
        self.bind("<Leave>", lambda _: self.configure(image=ctk_img_outline), add="+")

    def disable(self):
        """Disable the button."""
        img_disabled_light = Image.open(
            os.path.join(
                DIRNAME,
                f"assets/clipboard_icons/{self._type}/{self._type}-disabled-light.png",
            )
        )
        img_disabled_dark = Image.open(
            os.path.join(
                DIRNAME,
                f"assets/clipboard_icons/{self._type}/{self._type}-disabled-dark.png",
            )
        )
        ctk_img_outline_disabled = ctk.CTkImage(
            img_disabled_light,
            img_disabled_dark,
            size=(CLIPB_TOOLBAR_IMAGE_WIDTH, CLIPB_TOOLBAR_IMAGE_HEIGHT),
        )

        self.configure(image=ctk_img_outline_disabled, state="disabled")
        self.unbind("<Enter>")
        self.unbind("<Leave>")

        # the methods above also unbind the tooltip, so it has to be rebound
        if tooltip:
            self.bind("<Enter>", self.tooltip.on_enter)
            self.bind("<Leave>", self.tooltip.on_leave)
