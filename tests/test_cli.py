"""Test the CLI."""

import subprocess
import sys

import pytest
from PIL import ExifTags, Image

from exif_stripper import cli


@pytest.fixture
def image_with_exif_data(tmp_path):
    """Fixture for an image with EXIF data."""
    image_file = tmp_path / 'test.png'
    with Image.new(mode='1', size=(2, 2)) as im:
        exif = im.getexif()
        exif[274] = 2
        exif[ExifTags.IFD.GPSInfo] = {ExifTags.GPS.GPSVersionID: 1}
        im.save(image_file, exif=exif)

    return image_file


def has_metadata(filepath, gps_only) -> bool:
    """Utility to check if a file has metadata."""
    with Image.open(filepath) as im:
        exif = im.getexif()
        if gps_only:
            return ExifTags.IFD.GPSInfo in exif
        return bool(exif)


@pytest.mark.parametrize('gps_only', [True, False])
def test_process_image_full(monkeypatch, image_with_exif_data, gps_only):
    """Test that cli.process_image() removes the appropriate EXIF metadata."""
    assert has_metadata(image_with_exif_data, gps_only=False)

    has_changed = cli.process_image(image_with_exif_data, gps_only=gps_only)

    assert not has_metadata(image_with_exif_data, gps_only=gps_only)
    assert has_changed

    has_changed = cli.process_image(image_with_exif_data, gps_only=gps_only)
    assert not has_changed


@pytest.mark.parametrize('exists', [True, False])
@pytest.mark.parametrize('gps_only', [True, False])
def test_process_image_file_issues(tmp_path, exists, gps_only):
    """Test that cli.process_image() continues if files don't exist or aren't images."""
    file = tmp_path / 'test.txt'
    if exists:
        file.touch()

    has_changed = cli.process_image(file, gps_only)
    assert not has_changed


@pytest.mark.parametrize('gps_only', [True, False])
def test_main(capsys, tmp_path, image_with_exif_data, gps_only):
    """Test that cli.main() returns the number of files altered."""
    file_without_metadata = tmp_path / 'clean.png'
    file_without_metadata.touch()

    cli_args = [str(file_without_metadata), str(image_with_exif_data)]
    if gps_only:
        cli_args = ['--gps-only', *cli_args]

    files_changed = cli.main(cli_args)

    assert files_changed == 1
    assert not has_metadata(image_with_exif_data, gps_only=gps_only)

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
