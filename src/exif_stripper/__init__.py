"""EXIF stripper."""

from __future__ import annotations

import importlib.metadata
from contextlib import suppress
from typing import TYPE_CHECKING

from PIL import ExifTags, Image, UnidentifiedImageError

if TYPE_CHECKING:
    import os

__version__ = importlib.metadata.version(__name__)


def process_image(filename: str | os.PathLike, gps_only: bool) -> bool:
    """
    Process image EXIF metadata.

    Parameters
    ----------
    filename : str | os.PathLike
        The image file to check.
    gps_only : bool
        Whether to only strip GPS-related EXIF metadata.

    Returns
    -------
    bool
        Indicator of whether metadata was stripped.
    """
    with (
        suppress(FileNotFoundError, UnidentifiedImageError),
        Image.open(filename) as image,
    ):
        if exif := image.getexif():
            if gps_only:
                try:
                    # delete all GPS info: https://github.com/python-pillow/Pillow/issues/9078
                    del exif[ExifTags.IFD.GPSInfo]
                except KeyError:
                    # GPS-only mode and there is no GPS metadata present
                    return False
            else:
                exif.clear()

            image.save(filename, exif=exif)
            print(f'Stripped EXIF metadata from {filename}')
            return True

    return False
