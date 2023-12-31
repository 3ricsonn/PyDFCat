# -*- coding: utf-8 -*-
import os


DIRNAME = os.path.dirname(__file__)

# windows properties
WINDOW_RATIO = 0.9423076923076923
WINDOW_MIN_WIDTH_FACTOR = 0.62
WINDOW_MIN_HEIGHT_FACTOR = 0.56

# import window properties
IMPORT_WINDOW_HEIGHT_RATIO = 2.057

# widgets properties
# page view
PAGE_X_PADDING = 5
PAGE_Y_PADDING = 7
PAGE_IPADDING = 5

# toolbar
TOOLBAR_HEIGHT = 40
TOOLBAR_PADDING = 5
# toolbar widgets
TOOLBAR_X_PADDING = 5
TOOLBAR_Y_PADDING = 5
TOOLBAR_WIDGET_WIDTH = TOOLBAR_HEIGHT - 2 * TOOLBAR_X_PADDING
TOOLBAR_WIDGET_HEIGHT = TOOLBAR_HEIGHT - 2 * TOOLBAR_Y_PADDING
TOOLBAR_COMBOBOX_WIDTH = 3 * TOOLBAR_WIDGET_WIDTH
TOOLBAR_WIDGET_BORDER_SPACING = 2
# toolbar widgets icons
TOOLBAR_IMAGE_WIDTH = TOOLBAR_WIDGET_WIDTH - 2 * TOOLBAR_WIDGET_BORDER_SPACING
TOOLBAR_IMAGE_HEIGHT = TOOLBAR_WIDGET_HEIGHT - 2 * TOOLBAR_WIDGET_BORDER_SPACING

# toolbar option
SCALING_FACTORS = ["100%", "75%", "50%", "25%"]

# sidebar
# clipboard toolbar
CLIPB_TOOLBAR_HEIGHT = 35
# clipboard toolbar widgets
CLIPB_TOOLBAR_PADDING = 5
CLIPB_TOOLBAR_WIDGET_WIDTH = CLIPB_TOOLBAR_HEIGHT - 2 * CLIPB_TOOLBAR_PADDING
CLIPB_TOOLBAR_WIDGET_HEIGHT = CLIPB_TOOLBAR_HEIGHT - 2 * CLIPB_TOOLBAR_PADDING
CLIPB_TOOLBAR_WIDGET_BORDER_SPACING = 1
# toolbar widgets icons
CLIPB_TOOLBAR_IMAGE_WIDTH = (
    CLIPB_TOOLBAR_WIDGET_WIDTH - 2 * CLIPB_TOOLBAR_WIDGET_BORDER_SPACING
)
CLIPB_TOOLBAR_IMAGE_HEIGHT = (
    CLIPB_TOOLBAR_WIDGET_HEIGHT - 2 * CLIPB_TOOLBAR_WIDGET_BORDER_SPACING
)

# colors
COLOR_CLOSE_RED = ("#C04C4B", "#A51F27")
COLOR_SELECTED_BLUE = ("#3B8ED0", "#1F6AA5")
