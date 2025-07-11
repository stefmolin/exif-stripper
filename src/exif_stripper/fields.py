"""EXIF metadata fields."""

from enum import IntEnum, StrEnum, auto

from PIL import ExifTags

PRESERVE_FIELDS: tuple[IntEnum] = (
    ExifTags.Base.InterColorProfile,
    ExifTags.Base.Orientation,
)
"""Locations of EXIF information that should be preserved."""

OWNERSHIP_FIELDS: tuple[IntEnum] = (
    ExifTags.Base.Artist,
    ExifTags.Base.Copyright,
)
"""Locations of EXIF information related to copyright/ownership."""


class FieldGroup(StrEnum):
    """Enum for groups of fields to target."""

    ALL = auto()
    """Field group for deleting all EXIF metadata."""

    CAMERA = auto()
    """Field group for EXIF tags containing the make and model of the camera."""

    COPYRIGHT = auto()
    """Field group for EXIF tags related to the creator of the image."""

    GPS = auto()
    """Field group for all GPS information in EXIF metadata."""

    LENS = auto()
    """Field group for EXIF tags containing the make and model of the lens."""

    SERIALS = auto()
    """Field group for EXIF tags containing serial numbers."""


# References for EXIF tags:
# - meanings: https://exiv2.org/tags.html
# - enums: https://pillow.readthedocs.io/en/stable/_modules/PIL/ExifTags.html
EXIF_TAG_MAPPING: dict[FieldGroup, tuple[IntEnum]] = {
    FieldGroup.CAMERA: (
        ExifTags.Base.Make,
        ExifTags.Base.Model,
        ExifTags.Base.MakerNote,
        ExifTags.Base.MakerNoteSafety,
    ),
    FieldGroup.COPYRIGHT: OWNERSHIP_FIELDS,
    FieldGroup.GPS: (ExifTags.IFD.GPSInfo,),
    FieldGroup.LENS: (ExifTags.Base.LensMake, ExifTags.Base.LensModel),
    FieldGroup.SERIALS: (
        ExifTags.Base.BodySerialNumber,
        ExifTags.Base.CameraSerialNumber,
        ExifTags.Base.LensSerialNumber,
    ),
}
"""Mapping of FieldGroup to the corresponding locations in the EXIF metadata."""
