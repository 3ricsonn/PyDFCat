# -*- coding: utf-8 -*-
from typing import Any, Callable

import customtkinter as ctk
import os
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk

from .settings import (
    COLOR_CLOSE_RED,
    DIRNAME,
    SCALING_FACTORS,
    TOOLBAR_COMBOBOX_WIDTH,
    TOOLBAR_IMAGE_HEIGHT,
    TOOLBAR_IMAGE_WIDTH,
    TOOLBAR_WIDGET_BORDER_SPACING,
    TOOLBAR_WIDGET_HEIGHT,
    TOOLBAR_WIDGET_WIDTH,
    TOOLBAR_X_PADDING,
    TOOLBAR_Y_PADDING,
)


try:
    from CTkToolTip import CTkToolTip

    tooltip = True
except ModuleNotFoundError:
    tooltip = False


class ToolBar(ctk.CTkFrame):
    """Collection of tools to manipulate the pdf file pages."""

    def __init__(
        self,
        parent: Any,
        save_file_command: Callable,
        open_file_command: Callable,
        close_file_command: Callable,
        scale_page_command: Callable,
        scaling_variable: ctk.StringVar,
        **kwargs,
    ) -> None:
        """
        Initialize the ToolBar.

        Args:
            parent (Any): The parent widget.
            save_file_command (Callable): The command to save the file.
            open_file_command (Callable): The command to open a file.
            scale_page_command (Callable): The command to scale the page.
            scaling_variable (ctk.StringVar): The variable for scaling selection.
            **kwargs: Configuration arguments for ctk.CTkFrame.
        """
        super().__init__(master=parent, **kwargs)

        # functions
        self.close_file_command = close_file_command

        # file widgets
        # Open button
        self.open_button = ToolBarButton(
            self, "open", command=open_file_command, tooltip_message="open file"
        )
        self.open_button.pack(
            side="left", padx=TOOLBAR_X_PADDING, pady=TOOLBAR_Y_PADDING
        )

        # Save button with an option menu
        self.save_option_menu = SaveOptionMenu(
            self, command=save_file_command, tooltip_message="save file"
        )
        self.save_option_menu.pack(
            side="left", padx=TOOLBAR_X_PADDING, pady=TOOLBAR_Y_PADDING
        )

        # Undo button (initially disabled)
        self.undo_button = ToolBarButton(
            self,
            "undo",
            command=lambda: print("undone"),
            state="disabled",
            tooltip_message="undo",
        )
        self.undo_button.pack(
            side="left", padx=TOOLBAR_X_PADDING, pady=TOOLBAR_Y_PADDING
        )

        # Redo button (initially disabled)
        self.redo_button = ToolBarButton(
            self,
            "redo",
            command=lambda: print("redo_button"),
            state="disabled",
            tooltip_message="redo",
        )
        self.redo_button.pack(
            side="left", padx=TOOLBAR_X_PADDING, pady=TOOLBAR_Y_PADDING
        )

        # Scaling combobox (initially disabled)
        self.scaling_combobox = ctk.CTkComboBox(
            self,
            values=SCALING_FACTORS,
            command=scale_page_command,
            variable=scaling_variable,
            state="disabled",
            height=TOOLBAR_WIDGET_HEIGHT,
            width=TOOLBAR_COMBOBOX_WIDTH,
        )
        self.scaling_combobox.set(scaling_variable.get())
        if tooltip:
            CTkToolTip(self.scaling_combobox, message="page scaling")
        self.scaling_combobox.bind(
            "<Return>", lambda event: scale_page_command(scaling_variable.get())
        )
        self.scaling_combobox.pack(
            side="left", padx=TOOLBAR_X_PADDING, pady=TOOLBAR_Y_PADDING
        )

        # spacing
        ctk.CTkLabel(self, text="", fg_color="transparent").pack(
            side="left", expand=True
        )

        # edit widgets
        # cut button: cut pages to clipboard (initially disabled)
        self.cut_button = ToolBarButton(
            self,
            "cut",
            command=lambda: print("cut pages"),
            state="disabled",
            tooltip_message="cut to clipboard",
        )
        self.cut_button.pack(
            side="left", padx=TOOLBAR_X_PADDING, pady=TOOLBAR_Y_PADDING
        )

        # copy button: copy pages to clipboard (initially disabled)
        self.copy_button = ToolBarButton(
            self,
            "copy",
            command=lambda: print("copied pages"),
            state="disabled",
            tooltip_message="copy to clipboard",
        )
        self.copy_button.pack(
            side="left", padx=TOOLBAR_X_PADDING, pady=TOOLBAR_Y_PADDING
        )

        # past button: past pages from clipboard (initially disabled)
        self.past_button = ToolBarButton(
            self,
            "past",
            command=lambda: print("past pages"),
            state="disabled",
            tooltip_message="past from clipboard",
        )
        self.past_button.pack(
            side="left", padx=TOOLBAR_X_PADDING, pady=TOOLBAR_Y_PADDING
        )

        # duplicate button (initially disabled)
        self.duplicate_button = ToolBarButton(
            self,
            "duplicate",
            command=lambda: print("duplicate"),
            state="disabled",
            tooltip_message="duplicate selection",
        )
        self.duplicate_button.pack(
            side="left", padx=TOOLBAR_X_PADDING, pady=TOOLBAR_Y_PADDING
        )

        # delete button; delete page (initially disabled)
        self.delete_button = ToolBarButton(
            self,
            "delete",
            command=lambda: print("delete"),
            state="disabled",
            tooltip_message="delete selection",
        )
        self.delete_button.pack(
            side="left", padx=TOOLBAR_X_PADDING, pady=TOOLBAR_Y_PADDING
        )

        # spacing
        ctk.CTkLabel(self, text="", fg_color="transparent").pack(
            side="left", expand=True
        )

        # close dokument button (initially disabled)
        self.close_button = ToolBarButton(
            self,
            "close",
            hover_color=COLOR_CLOSE_RED,
            command=self._ask_close_file,
            tooltip_message="close document",
        )

    def _ask_close_file(self):
        """Opens a message to confirm closing."""
        msg = CTkMessagebox(
            title="Close Document",
            icon="question",
            message="Do you want to close your document?",
            option_1="no",
            option_2="yes",
        )
        response = msg.get()

        if response == "yes":
            self.close_file_command()

    def enable_all(self):
        """Enable the toolbar tools."""
        self.open_button.enable()
        self.save_option_menu.enable()
        self.undo_button.enable()
        self.redo_button.enable()
        self.scaling_combobox.configure(state="normal")
        self.close_button.pack(
            side="right", padx=TOOLBAR_X_PADDING, pady=TOOLBAR_Y_PADDING
        )

    def enable_open(self):
        """Only enables the open button."""
        self.open_button.enable()

    def disable_all_except_open(self):
        """Disable the toolbar tools except the open button."""
        self.save_option_menu.disable()
        self.undo_button.disable()
        self.redo_button.disable()

        self.scaling_combobox.configure(state="disabled")

        self.close_button.pack_forget()
        self.update_idletasks()

    def disable_all(self):
        """Disable all tools."""
        self.open_button.disable()
        self.disable_all_except_open()


class ToolBarButton(ctk.CTkButton):
    """
    A custom toolbar button class.

    This class inherits from ctk.CTkButton, a custom Tkinter Button class.
    """

    def __init__(self, parent: Any, button_type: str, tooltip_message="", **kwargs):
        """
        Initialize the ToolBarButton.

        Args:
            parent: The parent widget.
            button_type (str): The type of the button.
            tooltip_message (str, optional):
                The tooltip message for the button.
                Default is an empty string.
            **kwargs: Configuration arguments for CTkButton.
        """
        super().__init__(
            master=parent,
            text="",
            width=TOOLBAR_WIDGET_WIDTH,
            height=TOOLBAR_WIDGET_HEIGHT,
            border_spacing=TOOLBAR_WIDGET_BORDER_SPACING,
            **kwargs,
        )

        self._button_type = button_type
        self._tooltip_message = tooltip_message
        if tooltip:
            self.tooltip: CTkToolTip = CTkToolTip(self, message=self._tooltip_message)

        if "state" in kwargs and kwargs["state"] == "disabled":
            self.disable()
        else:
            self.enable()

            # bind tooltips to the icons
            if tooltip:
                self.bind("<Enter>", self.tooltip.on_enter)
                self.bind("<Leave>", self.tooltip.on_leave)

    def enable(self):
        """Enable the button."""
        img_outline = Image.open(
            os.path.join(
                DIRNAME,
                f"assets/toolbar_icons/{self._button_type}/{self._button_type}-outline.png",
            )
        )
        ctk_img_outline = ctk.CTkImage(
            img_outline,
            img_outline,
            size=(TOOLBAR_IMAGE_WIDTH, TOOLBAR_IMAGE_HEIGHT),
        )
        img_solid = Image.open(
            os.path.join(
                DIRNAME,
                f"assets/toolbar_icons/{self._button_type}/{self._button_type}-solid.png",
            )
        )
        ctk_img_solid = ctk.CTkImage(
            img_solid,
            img_solid,
            size=(TOOLBAR_IMAGE_WIDTH, TOOLBAR_IMAGE_HEIGHT),
        )

        self.configure(image=ctk_img_outline, state="normal")
        self.bind("<Enter>", lambda _: self.configure(image=ctk_img_solid), add="+")
        self.bind("<Leave>", lambda _: self.configure(image=ctk_img_outline), add="+")

    def disable(self):
        """Disable the button."""
        img_disabled_light = Image.open(
            os.path.join(
                DIRNAME,
                f"assets/toolbar_icons/{self._button_type}/{self._button_type}-disabled-light.png",
            )
        )
        img_disabled_dark = Image.open(
            os.path.join(
                DIRNAME,
                f"assets/toolbar_icons/{self._button_type}/{self._button_type}-disabled-dark.png",
            )
        )
        ctk_img_outline_disabled = ctk.CTkImage(
            img_disabled_light,
            img_disabled_dark,
            size=(TOOLBAR_IMAGE_WIDTH, TOOLBAR_IMAGE_HEIGHT),
        )

        self.configure(image=ctk_img_outline_disabled, state="disabled")
        self.unbind("<Enter>")
        self.unbind("<Leave>")

        # the methods above also unbind the tooltip, so it has to be rebound
        if tooltip:
            self.bind("<Enter>", self.tooltip.on_enter)
            self.bind("<Leave>", self.tooltip.on_leave)


class SaveOptionMenu(ctk.CTkOptionMenu):
    """
    A custom option menu for saving options.

    This class inherits from ctk.CTkOptionMenu, a custom Tkinter OptionMenu class.
    """

    def __init__(self, parent: Any, command: Callable, tooltip_message=""):
        """
        Initialize the SaveOptionMenu.

        Args:
            parent (Any): The parent widget.
            command (Callable): The function to be executed on option selection.
            tooltip_message (str, optional):
                The tooltip message for the option menu.
                Default is an empty string.
        """
        super().__init__(
            master=parent,
            values=["save", "save as"],
            command=command,
            width=TOOLBAR_WIDGET_WIDTH,
            height=TOOLBAR_WIDGET_HEIGHT,
        )

        if tooltip:
            self.tooltip: CTkToolTip = CTkToolTip(self, message=tooltip_message)

        self.disable()

    def _add_image_to_tk_label(self, img: ImageTk):
        """Add image to the option menu."""
        self._text_label.configure(image=img)
        self._text_label.image = img

    def enable(self):
        """Enable the option menu."""
        self.configure(state="normal")
        img_save_solid = Image.open(
            os.path.join(DIRNAME, "assets/toolbar_icons/save/save-outline.png")
        )
        img_save_solid = img_save_solid.resize(
            (TOOLBAR_IMAGE_WIDTH, TOOLBAR_IMAGE_HEIGHT)
        )
        tk_img_save_outline = ImageTk.PhotoImage(img_save_solid)
        img_save_solid = Image.open(
            os.path.join(DIRNAME, "assets/toolbar_icons/save/save-solid.png")
        )
        img_save_solid = img_save_solid.resize(
            (TOOLBAR_IMAGE_WIDTH, TOOLBAR_IMAGE_HEIGHT)
        )
        tk_img_save_solid = ImageTk.PhotoImage(img_save_solid)
        self._add_image_to_tk_label(tk_img_save_outline)
        self.bind(
            "<Enter>",
            lambda _: self._add_image_to_tk_label(tk_img_save_solid),
        )
        self.bind(
            "<Leave>",
            lambda _: self._add_image_to_tk_label(tk_img_save_outline),
        )

    def disable(self):
        """Disable the option menu."""
        self.configure(state="disabled")

        if ctk.get_appearance_mode() == "light":
            img_save_disabled = Image.open(
                os.path.join(
                    DIRNAME, "assets/toolbar_icons/save/save-disabled-light.png"
                )
            )
        else:
            img_save_disabled = Image.open(
                os.path.join(
                    DIRNAME, "assets/toolbar_icons/save/save-disabled-dark.png"
                )
            )
        img_save_disabled = img_save_disabled.resize(
            (TOOLBAR_IMAGE_WIDTH, TOOLBAR_IMAGE_HEIGHT)
        )
        tk_img_save_disabled = ImageTk.PhotoImage(img_save_disabled)
        self._add_image_to_tk_label(tk_img_save_disabled)
        self.unbind("<Enter>")
        self.unbind("<Leave>")

        # the methods above also unbind the tooltip
        if tooltip:
            self.bind("<Enter>", self.tooltip.on_enter)
            self.bind("<Leave>", self.tooltip.on_leave)
