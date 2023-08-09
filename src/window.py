# -*- coding: utf-8 -*-
import crossfiledialog
import customtkinter as ctk
import fitz  # PyMuPDF
import os
from maineditor import MainEditor
from settings import COLOR_CLOSE_RED, WHITE
from sidepanel import SidePanel
from toolbar import ToolBar


class ApplicationWindow(ctk.CTk):
    """Application window class"""

    def __init__(self,):
        """Create and configure the application window"""
        super().__init__()

        # layout
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # data
        scaling_variable = ctk.StringVar(value="100%")

        # main editor
        self.main_editor = MainEditor(
            self, open_file_command=self.open_file, scaling_variable=scaling_variable
        )
        self.main_editor.grid(column=1, row=1, sticky="news", padx=10, pady=10)

        # sidebar
        self.sidebar = SidePanel(self, jump_to_page_command=self.main_editor.jump_to_page)
        self.sidebar.grid(column=0, row=1, sticky="news", padx=10, pady=10)

        # close dokument button
        self.close_button = ctk.CTkButton(
            self,
            text="x",
            text_color=WHITE,
            fg_color="transparent",
            hover_color=COLOR_CLOSE_RED,
            width=40,
            height=40,
            command=self.close_file,
        )

        # toolbar
        self.toolbar = ToolBar(
            self,
            open_file_command=self.open_file,
            save_file_command=lambda _: print("save file"),
            scale_page_command=self.main_editor.update_scaling,
            scaling_variable=scaling_variable,
            height=60,
        )
        # ctk.CTkLabel(self.toolbar, text="Toolbar").place(relx=0.5, rely=0.5, anchor="center")
        self.toolbar.grid(column=0, row=0, columnspan=2, sticky="news")

        # self.main_editor.bind(
        #     "<Configure>",
        #    lambda _: print(
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
        file_name = crossfiledialog.open_file(
            title="Choose your PDF you want to edit:")

        if not file_name:
            return

        if has_file_extension(file_name, ".pdf"):
            # Load the selected PDF file using fitz
            pdf_document = fitz.Document(file_name)

            # Update the PDF document in the main editor and sidebar
            self.main_editor.get_new_document(pdf_document)
            self.sidebar.get_new_document(pdf_document)
            self.toolbar.enable_tools()

            # Update the application title with the file name
            self.title(f"PyDFCat - Editing: {os.path.basename(file_name)}")

            # Place the close button in the top right corner
            self.close_button.place(relx=0.97, rely=0.05, anchor="ne")
        else:
            # user selected a non-pdf file
            self.main_editor.open_file_error()

    def close_file(self):
        """CLose the file and discard all changes"""
        self.main_editor.close_document()
        self.sidebar.close_document()
        self.toolbar.disable_tools()

        self.title("PyDFCat")
        self.close_button.place_forget()


def has_file_extension(file_name: str, extension: str) -> bool:
    """
    Check if the file name has the specified file extension.

    Args:
        file_name (str): The file name to check.
        extension (str): The desired file extension (e.g., ".txt").

    Returns:
        bool: True if the file name has the specified extension, False otherwise.
    """
    file_extension = os.path.splitext(file_name)[1]
    return file_extension.lower() == extension.lower()
