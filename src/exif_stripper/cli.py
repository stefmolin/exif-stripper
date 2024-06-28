"""Tool for stripping image metadata (EXIF)."""

from __future__ import annotations

import argparse
import os
import platform
from typing import Sequence

from PIL import Image, UnidentifiedImageError

from . import __version__

PROG = 'strip-exif'


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


def main(argv: Sequence[str] | None = None) -> int:
    """
    Tool for stripping EXIF data from images.

    Parameters
    ----------
    argv : Sequence[str] | None, optional
        The arguments passed on the command line.

    Returns
    -------
    int
        Exit code for the process: if metadata was stripped,
        this will be 1 to stop a commit as a pre-commit hook.
    """
    parser = argparse.ArgumentParser(prog=PROG)
    parser.add_argument(
        'filenames',
        nargs='*',
        help='Filenames to process.',
    )
    parser.add_argument(
        '--version', action='version', version=f'%(prog)s {__version__}'
    )
    args = parser.parse_args(argv)

    results = [process_image(filename) for filename in args.filenames]
    return int(any(results))


if __name__ == '__main__':
    raise SystemExit(main())
