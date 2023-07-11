# -*- coding: utf-8 -*-
from typing import Any, Callable

import customtkinter as ctk
from settings import SCALING_FACTORS


class ToolBar(ctk.CTkFrame):
    def __init__(
        self,
        parent: Any,
        save_file_command: Callable,
        open_file_command: Callable,
        scale_page_command: Callable,
        scaling_variable: ctk.StringVar,
        **kwargs
    ) -> None:
        """
        Initialize the ToolBar.

        Args:
            parent (Any): The parent widget.
            save_file_command (Callable): The command to save the file.
            open_file_command (Callable): The command to open a file.
            scale_page_command (Callable): The command to scale the page.
            scaling_variable (ctk.StringVar): The variable for scaling selection.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(master=parent, **kwargs)

        # Open button
        ctk.CTkButton(self, text="Open", command=open_file_command, width=50).pack(side="left", padx=5, pady=7)

        # Save button with option menu
        ctk.CTkOptionMenu(self, values=["save", "save as"], command=save_file_command).pack(side="left", padx=5, pady=7)

        # Undo button (initially disabled)
        self.undo_button = ctk.CTkButton(self, text="Undo", command=lambda: print("undone"), width=50, state="disabled")
        self.undo_button.pack(side="left", padx=5, pady=7)

        # Redo button (initially disabled)
        self.redo_button = ctk.CTkButton(self, text="Redo", command=lambda: print("redone"), width=50, state="disabled")
        self.redo_button.pack(side="left", padx=5, pady=7)

        # Scaling combobox (initially disabled)
        self.scaling_combobox = ctk.CTkComboBox(
            self,
            values=SCALING_FACTORS,
            command=scale_page_command,
            variable=scaling_variable,
            state="disabled"
        )
        self.scaling_combobox.set(scaling_variable.get())
        self.scaling_combobox.pack(side="left", padx=5, pady=7)

    def enable_tools(self):
        """Enable the toolbar tools."""
        self.undo_button.configure(state="normal")
        self.redo_button.configure(state="normal")
        self.scaling_combobox.configure(state="normal")

    def disable_tools(self):
        """Disable the toolbar tools."""
        self.undo_button.configure(state="disabled")
        self.redo_button.configure(state="disabled")
        self.scaling_combobox.configure(state="disabled")
