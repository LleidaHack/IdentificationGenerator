"""
Constants module for truly constant values that don't change across environments.
Includes colors, font sizes, and other fixed configuration values.
"""
from typing import Tuple

# Font Sizes
TYPE_FONT_SIZE: int = 40
NAME_FONT_SIZE: int = 60

# Colors (RGB tuples)
FONT_COLOR: Tuple[int, int, int] = (0, 0, 0)
WHITE_FONT_COLOR: Tuple[int, int, int] = (84, 49, 26)
DARK_FONT_COLOR: Tuple[int, int, int] = (35, 35, 35)
BROWN_COLOR: Tuple[int, int, int] = (101, 67, 33)
MAIN_COLOR: Tuple[int, int, int] = (31, 33, 36)
BAK_COLOR: Tuple[int, int, int] = (119, 177, 201)

# QR Code Settings
QR_VERSION: int = 2
QR_BOX_SIZE: int = 10
QR_BORDER: int = 4
