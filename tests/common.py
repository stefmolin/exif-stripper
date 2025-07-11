"""Utility functions for testing."""

from PIL import Image

from exif_stripper.fields import (
    EXIF_TAG_MAPPING,
    OWNERSHIP_FIELDS,
    PRESERVE_FIELDS,
    FieldGroup,
)


def has_expected_metadata(filepath, fields, has_copyright, was_stripped) -> bool:
    """Utility to check if a file has the expected metadata."""
    with Image.open(filepath) as im:
        exif = im.getexif()

        preserved_fields_are_present = all(
            tag in exif for tag in PRESERVE_FIELDS
        ) and has_copyright == all(tag in exif for tag in OWNERSHIP_FIELDS)

        if fields is None or FieldGroup.ALL in fields:
            other_fields_present = all(
                tag in exif
                for field in set(FieldGroup).difference({FieldGroup.ALL})
                for tag in EXIF_TAG_MAPPING[field]
            )
            return preserved_fields_are_present and was_stripped != other_fields_present

        return preserved_fields_are_present and was_stripped != all(
            tag in exif for field in fields for tag in EXIF_TAG_MAPPING[field]
        )
