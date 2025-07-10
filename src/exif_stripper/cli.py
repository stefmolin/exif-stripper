"""Tool for stripping image metadata (EXIF)."""

from __future__ import annotations

import argparse
from typing import TYPE_CHECKING

from . import FieldGroup, __version__, process_image

if TYPE_CHECKING:
    from collections.abc import Sequence

PROG = 'exif-stripper'


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
        nargs='+',
        metavar='filename',
        help='filename to process',
    )
    parser.add_argument(
        '--version', action='version', version=f'%(prog)s {__version__}'
    )

    exif_options_group = parser.add_argument_group('data selection')
    exif_options_group.add_argument(
        '--fields',
        nargs='+',
        choices=list(FieldGroup),
        default=FieldGroup.ALL,
        help='the fields to remove from the EXIF metadata (all are removed by default)',
    )

    args = parser.parse_args(argv)

    results = [process_image(filename, args.fields) for filename in args.filenames]
    return int(any(results))


if __name__ == '__main__':
    raise SystemExit(main())
