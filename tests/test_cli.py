"""Test the CLI."""

import subprocess
import sys

import pytest
from PIL import ExifTags, Image

from exif_stripper import cli
from exif_stripper.exceptions import UnknownFieldError
from exif_stripper.fields import FIELDS, FieldGroup


@pytest.fixture
def image_with_exif_data(tmp_path):
    """Fixture for an image with EXIF data."""
    image_file = tmp_path / 'test.png'
    with Image.new(mode='1', size=(2, 2)) as im:
        exif = im.getexif()

        exif[ExifTags.IFD.GPSInfo] = {
            ExifTags.GPS.GPSVersionID: 1,
            ExifTags.GPS.GPSTrackRef: 1,
        }

        exif[ExifTags.Base.Make] = 'SomeCameraMake'
        exif[ExifTags.Base.Model] = 'SomeCameraModel'
        exif[ExifTags.Base.MakerNote] = 'Some maker notes'
        exif[ExifTags.Base.MakerNoteSafety] = 1

        exif[ExifTags.Base.LensMake] = 'SomeLensMake'
        exif[ExifTags.Base.LensModel] = 'SomeLensModel'

        exif[ExifTags.Base.BodySerialNumber] = 'ABC123'
        exif[ExifTags.Base.CameraSerialNumber] = 'DEF456'
        exif[ExifTags.Base.LensSerialNumber] = 'GHI789'

        im.save(image_file, exif=exif)

    return image_file


def has_metadata(filepath, fields) -> bool:
    """Utility to check if a file has metadata."""
    with Image.open(filepath) as im:
        exif = im.getexif()
        if fields is None or FieldGroup.ALL in fields:
            return bool(exif)
        return all(tag in exif for field in fields for tag in FIELDS[field])


@pytest.mark.parametrize(
    'fields',
    [
        [FieldGroup.ALL],
        [FieldGroup.ALL, FieldGroup.GPS],
        [FieldGroup.GPS],
        [FieldGroup.CAMERA, FieldGroup.LENS, FieldGroup.SERIALS],
    ],
)
def test_process_image_full(monkeypatch, image_with_exif_data, fields):
    """Test that cli.process_image() removes the appropriate EXIF metadata."""
    assert has_metadata(image_with_exif_data, fields)

    has_changed = cli.process_image(image_with_exif_data, fields=fields)

    assert not has_metadata(image_with_exif_data, fields)
    assert has_changed

    has_changed = cli.process_image(image_with_exif_data, fields=fields)
    assert not has_changed

    # make sure that the other fields haven't been touched
    if FieldGroup.ALL not in fields and (
        expected_untouched_groups := set(FieldGroup).difference(
            {FieldGroup.ALL, *fields}
        )
    ):
        assert has_metadata(image_with_exif_data, expected_untouched_groups)


def test_process_image_with_bad_field(image_with_exif_data):
    """Test that cli.process_image() raises an exception when provided with invalid fields."""
    with pytest.raises(UnknownFieldError):
        cli.process_image(image_with_exif_data, fields=['garbage'])


@pytest.mark.parametrize('exists', [True, False])
def test_process_image_file_issues(tmp_path, exists):
    """Test that cli.process_image() continues if files don't exist or aren't images."""
    file = tmp_path / 'test.txt'
    if exists:
        file.touch()

    has_changed = cli.process_image(file)
    assert not has_changed


@pytest.mark.parametrize(
    'fields',
    [
        None,
        [FieldGroup.ALL],
        [FieldGroup.ALL, FieldGroup.GPS],
        [FieldGroup.GPS],
        [FieldGroup.CAMERA, FieldGroup.LENS, FieldGroup.SERIALS],
    ],
)
def test_main(capsys, tmp_path, image_with_exif_data, fields):
    """Test that cli.main() returns the number of files altered."""
    file_without_metadata = tmp_path / 'clean.png'
    file_without_metadata.touch()

    cli_args = [str(file_without_metadata), str(image_with_exif_data)]
    if fields is not None:
        cli_args = ['--fields', *[str(field) for field in fields], '--', *cli_args]

    files_changed = cli.main(cli_args)

    assert files_changed == 1
    assert not has_metadata(image_with_exif_data, fields)

    assert capsys.readouterr().out.strip().endswith(str(image_with_exif_data))


def test_cli_version(capsys):
    """Confirm that --version works."""
    with pytest.raises(SystemExit):
        cli.main(['--version'])
    assert f'{cli.PROG} {cli.__version__}' == capsys.readouterr().out.strip()


@pytest.mark.parametrize(('flag', 'return_code'), [('--version', 0), ('', 1)])
def test_main_access_cli(flag, return_code, image_with_exif_data):
    """Confirm that CLI can be accessed via python -m."""
    result = subprocess.run(
        [sys.executable, '-m', 'exif_stripper.cli', flag or str(image_with_exif_data)]
    )
    assert result.returncode == return_code
