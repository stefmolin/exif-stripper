"""Test the CLI."""

import subprocess
import sys

import pytest
from PIL import Image

from exif_stripper import cli


@pytest.fixture
def image_with_exif_data(tmp_path):
    """Fixture for an image with EXIF data."""
    image_file = tmp_path / 'test.png'
    with Image.new(mode='1', size=(2, 2)) as im:
        exif = im.getexif()
        exif[274] = 2
        im.save(image_file, exif=exif)

    return image_file


def has_metadata(filepath) -> bool:
    """Utility to check if a file has metadata."""
    with Image.open(filepath) as im:
        return bool(im.getexif())


def test_process_image_full(image_with_exif_data, monkeypatch):
    """Test that cli.process_image() removes EXIF metadata."""
    assert has_metadata(image_with_exif_data)

    has_changed = cli.process_image(image_with_exif_data)

    assert not has_metadata(image_with_exif_data)
    assert has_changed

    has_changed = cli.process_image(image_with_exif_data)
    assert not has_changed


@pytest.mark.parametrize('exists', [True, False])
def test_process_image_file_issues(tmp_path, exists):
    """Test that cli.process_image() continues if files don't exist or aren't images."""
    file = tmp_path / 'test.txt'
    if exists:
        file.touch()

    has_changed = cli.process_image(file)
    assert not has_changed


def test_main(tmp_path, image_with_exif_data, capsys):
    """Test that cli.main() returns the number of files altered."""
    file_without_metadata = tmp_path / 'clean.png'
    file_without_metadata.touch()

    files_changed = cli.main([str(file_without_metadata), str(image_with_exif_data)])

    assert files_changed == 1

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
