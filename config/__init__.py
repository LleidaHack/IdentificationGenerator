"""
Configuration package for the Identification Generator.

Provides centralized access to settings, constants, and path management.
"""
from config.settings import settings, Settings
from config.constants import (
    TYPE_FONT_SIZE,
    NAME_FONT_SIZE,
    FONT_COLOR,
    WHITE_FONT_COLOR,
    DARK_FONT_COLOR,
    BROWN_COLOR,
    MAIN_COLOR,
    BAK_COLOR,
    QR_VERSION,
    QR_BOX_SIZE,
    QR_BORDER,
)
from config.paths import paths, PathManager

__all__ = [
    # Settings
    "settings",
    "Settings",
    # Constants
    "TYPE_FONT_SIZE",
    "NAME_FONT_SIZE",
    "FONT_COLOR",
    "WHITE_FONT_COLOR",
    "DARK_FONT_COLOR",
    "BROWN_COLOR",
    "MAIN_COLOR",
    "BAK_COLOR",
    "QR_VERSION",
    "QR_BOX_SIZE",
    "QR_BORDER",
    # Paths
    "paths",
    "PathManager",
]
