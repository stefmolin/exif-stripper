"""EXIF metadata fields."""

from enum import IntEnum, StrEnum, auto

from PIL import ExifTags


class FieldGroup(StrEnum):
    """Enum for groups of fields to target."""

    ALL = auto()
    CAMERA = auto()
    GPS = auto()
    LENS = auto()
    SERIALS = auto()


# References for EXIF tags:
# - meanings: https://exiv2.org/tags.html
# - enums: https://pillow.readthedocs.io/en/stable/_modules/PIL/ExifTags.html
FIELDS: dict[FieldGroup, tuple[IntEnum]] = {
    FieldGroup.CAMERA: (
        ExifTags.Base.Make,
        ExifTags.Base.Model,
        ExifTags.Base.MakerNote,
        ExifTags.Base.MakerNoteSafety,
    ),
    FieldGroup.GPS: (ExifTags.IFD.GPSInfo,),
    FieldGroup.LENS: (ExifTags.Base.LensMake, ExifTags.Base.LensModel),
    FieldGroup.SERIALS: (
        ExifTags.Base.BodySerialNumber,
        ExifTags.Base.CameraSerialNumber,
        ExifTags.Base.LensSerialNumber,
    ),
}
"""Mapping of FieldGroup to the corresponding locations in the EXIF metadata."""
