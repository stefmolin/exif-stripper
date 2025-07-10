"""Exceptions for exif_stripper."""

from enum import StrEnum


class UnknownFieldError(ValueError):
    """
    EXIF field is unknown to exif_stripper.

    Parameters
    ----------
    field : str
        The unknown field.
    options : StrEnum
        The enum of all known fields.
    """

    def __init__(self, field: str, options: StrEnum) -> None:
        super().__init__(f'Unknown field "{field}" -- options are {", ".join(options)}')
