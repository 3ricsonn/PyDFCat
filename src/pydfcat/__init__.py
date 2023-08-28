# -*- coding: utf-8 -*-
from optparse import OptionParser

import customtkinter
import os

from .settings import DIRNAME
from .window import ApplicationWindow


__version__ = "0.1.0-dev.2"


def start():
    """Start the program and process arguments from CLI"""
    usage_info = "usage %prog [options] [FILE]"
    version_info = f"%prog {__version__}"
    description = (
        "PyDFCat is a GUI PDF editor providing functionality to rearrange and "
        "delete pages within a PDF-file, as well as adding pages from other PDF-files"
    )
    parser = OptionParser(
        usage=usage_info, version=version_info, description=description
    )
    # parser.add_option()
    (_, args) = parser.parse_args()

    file_name = ""
    if len(args) > 1:
        parser.error("To many argument; expects one (FILE) or none")
    elif len(args) == 1:
        (file_name,) = args
        if not file_name and not os.path.isfile(file_name):
            parser.error(f"Couldn't find the provided file: {file_name}")

    customtkinter.set_default_color_theme(os.path.join(DIRNAME, "assets/ctktheme.json"))

    window = ApplicationWindow()

    # open file from cli argument
    if file_name:
        window.toolbar.disable_all()
        window.open_file(file_name)
        window.toolbar.enable_all()

    # run the windows mainloop
    window.mainloop()
