# -*- coding: utf-8 -*-
import customtkinter as ctk
from settings import (
    WINDOW_HEIGHT,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_WIDTH,
)
from widgets import CollapsableFrame, ScrollableFrame


class ApplicationWindow(ctk.CTk):
    """Application window class"""

    def __init__(self):
        """Create and configure the application window"""
        super().__init__()

        # window setup
        self.title("PDFCat")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # layout
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # toolbar
        self.toolbar = ctk.CTkFrame(self, fg_color="red", height=50)
        ctk.CTkLabel(self.toolbar, text="Toolbar").place(relx=0.5, rely=0.5, anchor="center")
        self.toolbar.grid(column=0, row=0, columnspan=2, sticky="news")

        # sidebar
        self.sidebar = CollapsableFrame(self, alignment="left")
        self.sidebar.grid(column=0, row=1, sticky="news")

        # main editor
        self.main_editor = ScrollableFrame(self)
        self.main_editor.grid(column=1, row=1, sticky="news")
