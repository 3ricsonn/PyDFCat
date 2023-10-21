# -*- coding: utf-8 -*-
import crossfiledialog
import customtkinter as ctk
import fitz  # PyMuPDF
import os
from io import BytesIO

from .importWIndow import ImportWindow
from .loadingWindow import LoadingWindow
from .maineditor import MainEditor
from .settings import (
    TOOLBAR_HEIGHT,
    TOOLBAR_PADDING,
    WINDOW_MIN_HEIGHT_FACTOR,
    WINDOW_MIN_WIDTH_FACTOR,
    WINDOW_RATIO,
)
from .sidepanel import SidePanel
from .toolbar import ToolBar


class ApplicationWindow(ctk.CTk):
    """Application window class."""

    def __init__(self):
        """Create and configure the application window."""
        super().__init__()

        # data
        self.file_name = ""
        self.main_document = fitz.Document()
        self.clipboard_document = fitz.Document()

        # window properties
        WINDOW_HEIGHT = self.winfo_screenheight()
        WINDOW_WIDTH = int(WINDOW_RATIO * WINDOW_HEIGHT)

        WINDOW_MIN_WIDTH = int(WINDOW_MIN_WIDTH_FACTOR * WINDOW_WIDTH)
        WINDOW_MIN_HEIGHT = int(WINDOW_MIN_HEIGHT_FACTOR * WINDOW_HEIGHT)

        # window setup
        self.title("PyDFCat")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # layout
        self.rowconfigure(0, minsize=TOOLBAR_HEIGHT + 2 * TOOLBAR_PADDING, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # data
        scaling_variable = ctk.StringVar(value="100%")

        # main editor
        self.main_editor = MainEditor(
            self,
            open_file_command=self.open_file_command,
            scaling_variable=scaling_variable,
        )
        self.main_editor.grid(column=1, row=1, sticky="news", padx=10, pady=10)

        # sidebar
        self.sidebar = SidePanel(
            self,
            jump_to_page_command=self.main_editor.jump_to_page,
            import_file_command=self.import_file_to_clipboard,
        )
        self.sidebar.grid(column=0, row=1, sticky="news", padx=10, pady=10)

        # toolbar
        self.toolbar = ToolBar(
            self,
            open_file_command=self.open_file_command,
            save_file_command=self.save_file_command,
            close_file_command=self.close_file,
            scale_page_command=self.main_editor.update_scaling,
            scaling_variable=scaling_variable,
            cut_command=self.cut_selection,
            copy_command=self.copy_selection,
            past_command=self.past_selection,
            duplicate_command=self.duplicate_selection,
            delete_command=self.delete_selection,
            height=TOOLBAR_HEIGHT,
        )
        self.toolbar.grid(
            column=0,
            row=0,
            columnspan=2,
            padx=TOOLBAR_PADDING,
            pady=TOOLBAR_PADDING,
            sticky="news",
        )

    def open_file_command(self) -> None:
        """Open a PDF file and load it into the PDF editor application."""
        self.toolbar.disable_all()
        self.sidebar.clipboard.disable_tools()

        # Open file dialog to select a PDF file
        file_name = crossfiledialog.open_file(
            title="Choose your PDF you want to edit:", filter={"PDF-Files": "*.pdf"}
        )

        if file_name:
            self.open_file(file_name)
        else:
            self.toolbar.open_button.enable()

    def open_file(self, file_name: str) -> None:
        """Opens and distributes the given document to the panels of the editor."""
        if has_file_extension(file_name, "pdf"):
            # Load the selected PDF file using fitz
            pdf_document = fitz.Document(file_name)

            loading_window = LoadingWindow(self, os.path.basename(file_name))

            # Update the PDF document in the main editor and sidebar
            self.main_editor.get_new_document(pdf_document, loading_window)
            self.sidebar.get_new_document(pdf_document, loading_window)

            loading_window.destroy()

            self.main_document = pdf_document
            self.clipboard_document = fitz.Document()

            # Update the application title with the file name
            self.title(f"PyDFCat - Editing: {os.path.basename(file_name)}")
            self.toolbar.enable_all()
            self.sidebar.clipboard.enable_all()
        else:
            # user selected a non-pdf file
            self.main_editor.open_file_error()
            self.toolbar.open_button.enable()

    def save_file_command(self, mode: str) -> None:
        """
        Save or prompt for a file name and location based on the chosen mode.

        Args:
            mode (str): The save mode, either "save" or "save as" to prompt for a new file name.

        If mode is "save" and a file name is already assigned, the document is saved without
        prompting.
        If mode is "save as" or no file name is assigned, a file dialog is shown for the user
        to choose a file name and location.

        The file is saved in PDF format.
        """
        if not (mode == "save" and self.file_name):
            file_name = crossfiledialog.save_file(
                title="Choose a file name and location for your file:"
            )
            if not file_name:
                return

            if not os.path.splitext(file_name)[1] == ".pdf":
                file_name += ".pdf"
            self.file_name = file_name

        self.main_document.save(self.file_name, garbage=4)

    def copy_selection(self) -> None:
        """
        Copy the selected content from the main editor to the clipboard.

        This method copies the selected pages from the main document and inserts them
        into the clipboard document, updating the clipboard and switching to the
        Clipboard tab in the sidebar.
        """
        # Get the page numbers of the selected content
        page_numbers = sorted(self.main_editor.get_selection())

        if page_numbers:
            # Get document pages and make a document copy
            doc_buffer = BytesIO(self.main_document.write(garbage=4))
            pages = fitz.Document(stream=doc_buffer, filetype="pdf")
            pages.select(page_numbers)

            # Insert selected pages into the clipboard document
            self.clipboard_document.insert_pdf(pages)

            # Switch to the Clipboard tab in the sidebar
            self.sidebar.tabview.set("Clipboard")

            # Update the clipboard with the copied pages
            self.sidebar.clipboard.insert_pages(-1, pages)

            # Clear the selection in the main editor
            self.main_editor.clear_selection()

    def cut_selection(self) -> None:
        """
        Cut the selected content from the main editor and place it in the clipboard.

        This method cuts the selected pages from the main document, inserts them into
        the clipboard document, and updates the editors and navigators accordingly.
        """
        # Get the page numbers of the selected content
        page_numbers = sorted(self.main_editor.get_selection())

        if page_numbers:
            # Get document pages and make a document copy
            doc_buffer = BytesIO(self.main_document.write(garbage=4))
            pages = fitz.Document(stream=doc_buffer, filetype="pdf")
            pages.select(page_numbers)

            # Insert selected pages into the clipboard document
            self.clipboard_document.insert_pdf(pages)

            # Delete the selected pages from the main document
            self.main_document.delete_pages(page_numbers)

            # Switch to the Clipboard tab in the sidebar
            self.sidebar.tabview.set("Clipboard")

            # Update the main editor, navigator, and clipboard
            self.main_editor.delete_pages(page_numbers)
            self.sidebar.navigator.delete_pages(page_numbers)
            self.sidebar.clipboard.insert_pages(-1, pages)

            # Clear the selection in the main editor
            self.main_editor.clear_selection()

    def past_selection(self) -> None:
        """
        Paste the selected content from the clipboard into the main document.

        This method selects content from the clipboard, inserts it into the
        main document, and updates the editors accordingly.
        """
        # Get the selected content from the main editor
        main_page_numbers = self.main_editor.get_selection()

        # If no content is selected, return
        if not main_page_numbers:
            return None

        # Determine the insert index for the clipboard content
        insert_index = max(main_page_numbers) + 1
        clipboard_page_numbers = sorted(self.sidebar.clipboard.get_selection())

        if clipboard_page_numbers:
            # Get document pages from the clipboard and make a document copy
            doc_buffer = BytesIO(self.clipboard_document.write(garbage=4))
            pages = fitz.Document(stream=doc_buffer, filetype="pdf")
            pages.select(clipboard_page_numbers)

            # Insert clipboard pages into the main document
            self.main_document.insert_pdf(pages, start_at=insert_index)

            # Update the main editor with the inserted pages
            self.main_editor.insert_pages(insert_index, pages)

            # Update the navigator in the sidebar
            self.sidebar.navigator.insert_pages(insert_index, pages)

            # Select the inserted range in the main editor
            self.main_editor.select_range(
                insert_index, insert_index + len(clipboard_page_numbers)
            )

            # Jump to the page where the clipboard content was inserted
            self.main_editor.jump_to_page(insert_index)

        return None

    def duplicate_selection(self):
        """
        Duplicate the selected content in the main editor.

        This method duplicates the selected pages in the main document and updates
        the editors and navigators accordingly.
        """
        # Get the page numbers of the selected content
        page_numbers = sorted(self.main_editor.get_selection())

        if page_numbers:
            # Duplicate the selected pages in the main document
            for page_number, n in enumerate(page_numbers):
                self.main_document.fullcopy_page(page_number + n, page_number + n + 1)

            # Update the main editor with duplicated pages
            self.main_editor.duplicate_pages(page_numbers)

            # Duplicate the pages in the sidebar navigator
            self.sidebar.navigator.duplicate_pages(page_numbers)

            # Clear the selection in the main editor
            self.main_editor.clear_selection()

    def delete_selection(self) -> None:
        """
        Delete the selected content from the main editor and the main document.

        This method deletes the selected pages from the main document and updates
        the editors and navigators accordingly.
        """
        # Get the page numbers of the selected content
        page_numbers = sorted(self.main_editor.get_selection())

        if page_numbers:
            # Delete the selected pages from the main document
            self.main_document.delete_pages(page_numbers)

            # Update the main editor with the deleted pages
            self.main_editor.delete_pages(page_numbers)

            # Delete the pages from the sidebar navigator
            self.sidebar.navigator.delete_pages(page_numbers)

            # Clear the selection in the main editor
            self.main_editor.clear_selection()

    def import_file_to_clipboard(self):
        self.toolbar.disable_all()
        self.sidebar.clipboard.disable_tools()

        # Open file dialog to select a PDF file
        file_name = crossfiledialog.open_file(
            title="Choose your PDF you want to import to your clipboard:",
            filter={"PDF-Files": "*.pdf"},
        )

        if file_name and has_file_extension(file_name, "pdf"):
            import_doc = fitz.Document(file_name)

            import_window = ImportWindow(
                self,
                lambda pages: self.import_file_to_clipboard_command(pages),
                self.enable_tools,
            )
            import_window.load_pages(import_doc)
        else:
            self.enable_tools()

    def import_file_to_clipboard_command(self, pages: fitz.Document) -> None:
        # import into clipboard
        self.sidebar.clipboard.insert_pages(-1, pages)

        # cleanup
        self.enable_tools()

    def enable_tools(self):
        # cleanup
        self.toolbar.enable_all()
        self.sidebar.clipboard.enable_all()

    def close_file(self):
        """CLose the file and discard all changes."""
        self.main_editor.close_document()
        self.sidebar.navigator.close_document()
        self.sidebar.clipboard.close_document()
        self.toolbar.disable_all_except_open()

        self.title("PyDFCat")


def has_file_extension(file_name: str, extension: str) -> bool:
    """
    Check if the file name has the specified file extension.

    Args:
        file_name (str): The file name to check.
        extension (str): The desired file extension (e.g. "txt").

    Returns:
        bool: True if the file name has the specified extension, False otherwise.
    """
    file_extension = os.path.splitext(file_name)[1]
    return file_extension.lower() == "." + extension.lower()
