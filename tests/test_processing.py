"""Test the image processing logic."""

import pytest

from exif_stripper.exceptions import UnknownFieldError
from exif_stripper.fields import FieldGroup
from exif_stripper.processing import process_image

from .common import has_expected_metadata


@pytest.mark.parametrize(
    ('fields', 'preserve_copyright'),
    [
        ([FieldGroup.ALL], True),
        ([FieldGroup.ALL, FieldGroup.GPS, FieldGroup.COPYRIGHT], False),
        ([FieldGroup.GPS, FieldGroup.COPYRIGHT], False),
        ([FieldGroup.CAMERA, FieldGroup.LENS, FieldGroup.SERIALS], True),
    ],
)
def test_process_image_full(
    capsys, monkeypatch, image_with_full_exif_data, fields, preserve_copyright
):
    """Test that process_image() removes the appropriate EXIF metadata."""
    assert has_expected_metadata(
        image_with_full_exif_data, fields, has_copyright=True, was_stripped=False
    )

    has_changed = process_image(image_with_full_exif_data, fields=fields)

    assert has_expected_metadata(
        image_with_full_exif_data,
        fields,
        has_copyright=preserve_copyright,
        was_stripped=True,
    )
    assert has_changed

    has_changed = process_image(image_with_full_exif_data, fields=fields)
    assert not has_changed

    # make sure that the other fields haven't been touched
    if FieldGroup.ALL not in fields and (
        expected_untouched_groups := set(FieldGroup).difference(
            {FieldGroup.ALL, *fields}
        )
    ):
        assert has_expected_metadata(
            image_with_full_exif_data,
            expected_untouched_groups,
            has_copyright=preserve_copyright,
            was_stripped=False,
        )


def test_process_image_with_bad_field(image_with_full_exif_data):
    """Test that process_image() raises an exception when provided with invalid fields."""
    with pytest.raises(UnknownFieldError):
        process_image(image_with_full_exif_data, fields=['garbage'])


@pytest.mark.parametrize('exists', [True, False])
def test_process_image_file_issues(tmp_path, exists):
    """Test that process_image() continues if files don't exist or aren't images."""
    file = tmp_path / 'test.txt'
    if exists:
        file.touch()

    has_changed = process_image(file)
    assert not has_changed


def test_process_image_does_not_always_rewrite(capsys, image_with_exif_data):
    """Test that process_image() doesn't rewrite the file if the EXIF data doesn't change."""
    has_changed = process_image(image_with_exif_data)
    assert not has_changed
    assert not capsys.readouterr().out.strip().endswith(str(image_with_exif_data))


def test_process_image_does_nothing_when_there_is_no_exif_data(
    capsys, image_without_exif_data
):
    """Test that process_image() does nothing when the file has no EXIF data."""
    has_changed = process_image(image_without_exif_data)
    assert not has_changed
    assert not capsys.readouterr().out.strip().endswith(str(image_without_exif_data))
