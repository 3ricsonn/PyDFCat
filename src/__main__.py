# -*- coding: utf-8 -*-
from settings import (
    WINDOW_MIN_HEIGHT_FACTOR,
    WINDOW_MIN_WIDTH_FACTOR,
    WINDOW_RATIO,
)
from window import ApplicationWindow


window = ApplicationWindow()

# window properties
WINDOW_HEIGHT = window.winfo_screenheight()
WINDOW_WIDTH = int(WINDOW_RATIO * WINDOW_HEIGHT)

WINDOW_MIN_WIDTH = int(WINDOW_MIN_WIDTH_FACTOR * WINDOW_WIDTH)
WINDOW_MIN_HEIGHT = int(WINDOW_MIN_HEIGHT_FACTOR * WINDOW_HEIGHT)

# window setup
window.title("PyDFCat")
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
window.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

# run the windows mainloop
window.mainloop()
