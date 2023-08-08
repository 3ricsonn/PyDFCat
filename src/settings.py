# -*- coding: utf-8 -*-
from screeninfo import get_monitors


# windows properties
screen = get_monitors()[0]
WINDOW_RATIO = 0.9296407185628742

WINDOW_HEIGHT = screen.height
WINDOW_WIDTH = int(WINDOW_RATIO * WINDOW_HEIGHT)

WINDOW_MIN_WIDTH = int(0.62 * WINDOW_WIDTH)
WINDOW_MIN_HEIGHT = int(0.56 * WINDOW_HEIGHT)

# widgets properties
PAGE_X_PADDING = 5
SCROLLBAR_WIDTH = 16  # TODO: Determent automatically?

# colors
BLACK = "#000"
WHITE = "#FFF"
CLOSE_RED = "#8A0606"

# toolbar option
SCALING_FACTORS = ["100%", "75%", "50%", "25%"]
