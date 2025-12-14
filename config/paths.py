"""
Path management module for constructing file paths and lazy-loading fonts.
"""
from os import path
from typing import Optional
from PIL import ImageFont

from config.settings import settings
from config.constants import TYPE_FONT_SIZE, NAME_FONT_SIZE


class PathManager:
    """Manages path construction and font loading."""
    
    def __init__(self):
        self._type_font: Optional[ImageFont.FreeTypeFont] = None
        self._name_font: Optional[ImageFont.FreeTypeFont] = None
        self._bold_type_font: Optional[ImageFont.FreeTypeFont] = None
        self._bold_name_font: Optional[ImageFont.FreeTypeFont] = None
    
    # Base Paths
    @property
    def out_path(self) -> str:
        """Output folder path."""
        return path.join('.', settings.OUT_FOLDER)
    
    @property
    def res_path(self) -> str:
        """Resources folder path."""
        return path.join('.', settings.RES_FOLDER)
    
    @property
    def data_path(self) -> str:
        """Data file path."""
        return path.join(
            self.res_path,
            settings.EDITIONS_FOLDER,
            settings.EDITION,
            settings.DATA_FILE
        )
    
    @property
    def db_cert_path(self) -> str:
        """Database certificate path."""
        return path.join(self.res_path, settings.DB_CERT)
    
    # Template Paths
    @property
    def bak_path_contestant(self) -> str:
        """Contestant card template path."""
        return path.join(
            self.res_path,
            settings.EDITIONS_FOLDER,
            settings.EDITION,
            settings.BAK_FILE_CONTESTANT
        )
    
    @property
    def bak_path_staff(self) -> str:
        """Staff card template path."""
        return path.join(
            self.res_path,
            settings.EDITIONS_FOLDER,
            settings.EDITION,
            settings.BAK_FILE_STAFF
        )
    
    @property
    def bak_path_empresa(self) -> str:
        """Company card template path."""
        return path.join(
            self.res_path,
            settings.EDITIONS_FOLDER,
            settings.EDITION,
            settings.BAK_FILE_EMPRESA
        )
    
    # Font Paths
    @property
    def font_path(self) -> str:
        """Regular font file path."""
        return path.join(self.res_path, settings.FONT_FOLDER, settings.FONT_FILE)
    
    @property
    def bold_font_path(self) -> str:
        """Bold font file path."""
        return path.join(self.res_path, settings.FONT_FOLDER, settings.BOLD_FONT_FILE)
    
    # Lazy-loaded Fonts
    @property
    def type_font(self) -> ImageFont.FreeTypeFont:
        """Regular type font (lazy-loaded)."""
        if self._type_font is None:
            self._type_font = ImageFont.truetype(self.font_path, TYPE_FONT_SIZE)
        return self._type_font
    
    @property
    def name_font(self) -> ImageFont.FreeTypeFont:
        """Regular name font (lazy-loaded)."""
        if self._name_font is None:
            self._name_font = ImageFont.truetype(self.font_path, NAME_FONT_SIZE)
        return self._name_font
    
    @property
    def bold_type_font(self) -> ImageFont.FreeTypeFont:
        """Bold type font (lazy-loaded)."""
        if self._bold_type_font is None:
            self._bold_type_font = ImageFont.truetype(self.bold_font_path, TYPE_FONT_SIZE)
        return self._bold_type_font
    
    @property
    def bold_name_font(self) -> ImageFont.FreeTypeFont:
        """Bold name font (lazy-loaded)."""
        if self._bold_name_font is None:
            self._bold_name_font = ImageFont.truetype(self.bold_font_path, NAME_FONT_SIZE)
        return self._bold_name_font


# Singleton instance
paths = PathManager()
