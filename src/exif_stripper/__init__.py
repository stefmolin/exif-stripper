"""EXIF stripper."""

from __future__ import annotations

import os
import platform

from PIL import Image, UnidentifiedImageError

__version__ = '0.5.0'


def process_image(filename: str | os.PathLike) -> bool:
    """
    Process image metadata.

    Parameters
    ----------
    filename : str | os.PathLike
        The image file to check.

    Returns
    -------
    bool
        Indicator of whether metadata was stripped.
    """
    has_changed = False
    try:
        # remove EXIF data
        with Image.open(filename) as im:
            if exif := im.getexif():
                exif.clear()
                im.save(filename)
                has_changed = True
    except (FileNotFoundError, UnidentifiedImageError):
        pass  # not an image
    else:
        # remove extended attributes (Unix only)
        if platform.system() != 'Windows':
            from xattr import xattr

            xattr_obj = xattr(filename)
            if xattr_obj.list():
                xattr_obj.clear()
                has_changed = True

    if has_changed:
        print(f'Stripped metadata from {filename}')

    return has_changed
