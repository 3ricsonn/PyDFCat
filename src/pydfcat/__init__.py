# -*- coding: utf-8 -*-
import argparse

import customtkinter
import os

from .settings import DIRNAME
from .window import ApplicationWindow


__version__ = "0.1.0-dev.3"


def start():
    """Start the program and process arguments from CLI"""
    description = (
        "PyDFCat is a GUI PDF editor providing functionality to rearrange and "
        "delete pages within a PDF-file, as well as adding pages from other PDF-files"
    )
    parser = argparse.ArgumentParser(prog="pydfcat", description=description)
    parser.add_argument(
        "filepath",
        nargs="?",
        help="path to the file to open in %(prog)s",
        metavar="FILE",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    if args.filepath and not os.path.isfile(args.filepath):
        parser.error(f"Couldn't find the provided file: {args.filepath}")

    customtkinter.set_default_color_theme(os.path.join(DIRNAME, "assets/ctktheme.json"))

    window = ApplicationWindow()

    # open file from cli argument
    if args.filepath:
        window.toolbar.disable_all()
        window.open_file(args.filepath)
        window.toolbar.enable_all()

    # run the windows mainloop
    window.mainloop()
