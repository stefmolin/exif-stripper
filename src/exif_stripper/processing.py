"""Image processing for exif_stripper."""

from __future__ import annotations

import itertools
from contextlib import suppress
from copy import deepcopy
from typing import TYPE_CHECKING

from PIL import Image, UnidentifiedImageError

from .exceptions import UnknownFieldError
from .fields import EXIF_TAG_MAPPING, OWNERSHIP_FIELDS, PRESERVE_FIELDS, FieldGroup

if TYPE_CHECKING:
    import os
    from collections.abc import Sequence


def process_image(
    filename: str | os.PathLike,
    fields: Sequence[FieldGroup] = (FieldGroup.ALL,),
) -> bool:
    """
    Process image EXIF metadata.

    Parameters
    ----------
    filename : str | os.PathLike
        The image file to check.
    fields : Sequence[FieldGroup], default ``(FieldGroup.ALL,)``
       The group of fields to check for and remove, if present.

    Returns
    -------
    bool
        Indicator of whether metadata was stripped.
    """
    has_changed = False

    with (
        suppress(FileNotFoundError, UnidentifiedImageError),
        Image.open(filename) as image,
    ):
        exif = image.getexif()

        if FieldGroup.ALL in fields:
            original_exif = deepcopy(exif)

            fields_to_preserve = {
                location: value
                for location in itertools.chain(
                    PRESERVE_FIELDS,
                    OWNERSHIP_FIELDS if FieldGroup.COPYRIGHT not in fields else {},
                )
                if (value := exif.get(location))
            }

            exif.clear()

            for field, value in fields_to_preserve.items():
                exif[field] = value

            has_changed = original_exif != exif
        else:
            for field in fields:
                if locations := EXIF_TAG_MAPPING.get(field):
                    for location in locations:
                        with suppress(KeyError):
                            del exif[location]
                            has_changed = True
                else:
                    raise UnknownFieldError(field, FieldGroup)

        if has_changed:
            image.save(filename, exif=exif)
            print(f'Stripped EXIF metadata from {filename}')

    return has_changed
