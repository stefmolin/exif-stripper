"""EXIF stripper."""

from __future__ import annotations

import os
from contextlib import suppress

from PIL import Image, UnidentifiedImageError

__version__ = '0.6.0'


def process_image(filename: str | os.PathLike) -> bool:
    """
    Process image EXIF metadata.

    Parameters
    ----------
    filename : str | os.PathLike
        The image file to check.

    Returns
    -------
    bool
        Indicator of whether metadata was stripped.
    """
    with suppress(FileNotFoundError, UnidentifiedImageError), Image.open(
        filename
    ) as image:
        if exif := image.getexif():
            exif.clear()
            image.save(filename)
            print(f'Stripped EXIF metadata from {filename}')
            return True
    return False
