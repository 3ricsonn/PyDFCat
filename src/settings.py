# -*- coding: utf-8 -*-
from screeninfo import get_monitors


# windows properties
screen = get_monitors()[0]
WINDOW_RATIO = 0.9423076923076923

WINDOW_HEIGHT = screen.height
WINDOW_WIDTH = int(WINDOW_RATIO * WINDOW_HEIGHT)

WINDOW_MIN_WIDTH = int(0.62 * WINDOW_WIDTH)
WINDOW_MIN_HEIGHT = int(0.56 * WINDOW_HEIGHT)

# widgets properties
PAGE_X_PADDING = 5
PAGE_Y_PADDING = 7
PAGE_IPADDING = 4

# colors
BLACK = "#000"
WHITE = "#FFF"
CLOSE_RED = "#8A0606"
SELECTED = "#1A73E8"

# toolbar option
SCALING_FACTORS = ["100%", "75%", "50%", "25%"]
