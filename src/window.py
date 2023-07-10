# -*- coding: utf-8 -*-
from tkinter.filedialog import askopenfilename

import customtkinter as ctk
import fitz  # PyMuPDF
import os
from maineditor import MainEditor
from settings import (
    CLOSE_RED,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_WIDTH,
)
from sidepanel import SidePanel


class ApplicationWindow(ctk.CTk):
    """Application window class"""

    def __init__(self):
        """Create and configure the application window"""
        super().__init__()

        # window setup
        self.title("PyDFCat")
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
        self.sidebar = SidePanel(self)
        self.sidebar.grid(column=0, row=1, sticky="news", padx=10, pady=10)

        # main editor
        self.main_editor = MainEditor(self, open_file_command=self.open_file)
        self.main_editor.grid(column=1, row=1, sticky="news", padx=10, pady=10)

        # close dokument button
        self.close_button = ctk.CTkButton(
            self,
            text="x",
            text_color=WHITE,
            fg_color="transparent",
            hover_color=CLOSE_RED,
            width=40,
            height=40,
            command=self.close_file
        )

        # self.main_editor.bind(
        #     "<Configure>",
        #     lambda _: print(
        #         self.main_editor.winfo_geometry()
        #         + " ("
        #         + self.winfo_geometry()
        #         + " - "
        #         + self.toolbar.winfo_geometry()
        #         + ")"
        #     )
        # )

    def open_file(self) -> None:
        """Open a PDF file and load it into the PDF editor application."""
        # Open file dialog to select a PDF file
        file_name = askopenfilename(
            title="Choose your PDF you want to edit:",
            filetypes=[("PDF-Files", "*.pdf")],
        )

        if file_name:
            # Load the selected PDF file using fitz
            pdf_document = fitz.Document(file_name)

            # Update the PDF document in the main editor and sidebar
            self.main_editor.get_new_document(pdf_document)
            self.sidebar.get_new_document(pdf_document)

            # Update the application title with the file name
            self.title(f"PyDFCat - Editing: {os.path.basename(file_name)}")

            # Place the close button in the top right corner
            self.close_button.place(relx=0.97, rely=0.05, anchor="ne")

    def close_file(self):
        self.main_editor.close_document()
        self.sidebar.close_document()

        self.title("PyDFCat")
        self.close_button.place_forget()
