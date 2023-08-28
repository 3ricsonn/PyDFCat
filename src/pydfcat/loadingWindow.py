# -*- coding: utf-8 -*-
from typing import Optional

import customtkinter as ctk


class LoadingWindow(ctk.CTkToplevel):
    """
    A custom loading window for indicating file loading progress.

    This class inherits from ctk.CTkToplevel, a custom Tkinter Toplevel class.
    """

    def __init__(self, parent, file_name: str, **kwargs):
        """
        Initialize the LoadingWindow.

        Args:
            parent: The parent widget.
            file_name (str): The name of the file being loaded.
            **kwargs: Configuration arguments for CTkTopLevel.
        """
        super().__init__(master=parent, **kwargs)

        # window setup
        self.title("Open file")
        self.geometry("200x75")
        self.resizable(False, False)

        # prevent closing the window
        self.protocol(
            "WM_DELETE_WINDOW", lambda: print("Don't close the loading window")
        )

        # data
        self.aimed_absolut = 1
        self.aimed_percentage = 1.0
        self.percentage = 0.0

        # widgets
        self.loading_bar = ctk.CTkProgressBar(self, width=100)
        self.loading_bar.set(0)
        self.loading_bar.pack(expand=True, side="top", fill="x", padx=10, pady=5)

        if len(file_name) > 20:
            text = file_name[:17] + "..."
        else:
            text = file_name

        ctk.CTkLabel(self, text=f"Open file {text}").pack(
            side="top", expand=True, fill="x", padx=10, pady=5
        )

    def aim(self, absolut: int, percentage: Optional[float] = None) -> None:
        """
        Set the loading aim.

        Args:
            absolut (int): The absolute value representing the loading aim.
            percentage (float, optional): The targeted loading percentage.
        """
        if percentage:
            self.aimed_percentage = percentage
        self.aimed_absolut = absolut

    def add(self) -> None:
        """Update the loading progress."""
        self.percentage += (1 / self.aimed_absolut) * self.aimed_percentage

        self.loading_bar.set(self.percentage)
        self.title(f"Open file ({int(self.percentage * 100)}%)")
