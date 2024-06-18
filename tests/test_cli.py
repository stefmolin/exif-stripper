"""Test the CLI."""

import platform
import subprocess
import sys
from getpass import getuser

import pytest
from PIL import Image

from exif_stripper import cli

RUNNING_ON = platform.system()
RUNNING_ON_WINDOWS = RUNNING_ON == 'Windows'

if not RUNNING_ON_WINDOWS:
    from xattr import xattr


@pytest.fixture
def image_with_exif_data(tmp_path):
    """Fixture for an image with EXIF data."""
    image_file = tmp_path / 'test.png'
    with Image.new(mode='1', size=(2, 2)) as im:
        exif = im.getexif()
        exif[274] = 2
        im.save(image_file, exif=exif)

    return image_file


@pytest.fixture
def image_with_metadata(image_with_exif_data):
    """Fixture for an image with metadata."""
    if RUNNING_ON in ['Darwin', 'Linux']:
        try:
            xattr(image_with_exif_data).set(
                f'{getuser()}.test_extended_attribute'
                if RUNNING_ON == 'Linux'
                else 'com.apple.macl',
                b'\x00',
            )
        except OSError:  # pragma: nocover
            # filesystem does not support extended attributes
            pass
    return image_with_exif_data


def has_metadata(filepath, on_windows):
    """Utility to check if a file has metadata."""
    with Image.open(filepath) as im:
        has_exif = dict(im.getexif()) != {}
        if on_windows:
            return has_exif
        return has_exif or xattr(filepath).list()


def assert_metadata_stripped(filepath, on_windows=RUNNING_ON_WINDOWS):
    """Checks that a file that had metadata before no longer does."""
    assert has_metadata(filepath, on_windows)

    has_changed = cli.process_image(filepath)

    assert not has_metadata(filepath, on_windows)
    assert has_changed

    has_changed = cli.process_image(filepath)
    assert not has_changed


@pytest.mark.skipif(RUNNING_ON_WINDOWS, reason='xattr does not work on Windows')
def test_process_image_full(image_with_metadata, monkeypatch):
    """Test that cli.process_image() removes EXIF and extended attributes."""
    assert_metadata_stripped(image_with_metadata)


def test_process_image_exif_only(image_with_exif_data, monkeypatch):
    """Test that cli.process_image() removes EXIF only (Windows version)."""
    if not RUNNING_ON_WINDOWS:
        monkeypatch.setattr(platform, 'system', lambda: 'Windows')
    assert_metadata_stripped(image_with_exif_data, on_windows=True)


@pytest.mark.parametrize('exists', [True, False])
def test_process_image_file_issues(tmp_path, exists):
    """Test that cli.process_image() continues if files don't exist or aren't images."""
    file = tmp_path / 'test.txt'
    if exists:
        file.touch()

    has_changed = cli.process_image(file)
    assert not has_changed


def test_main(tmp_path, image_with_metadata, capsys):
    """Test that cli.main() returns the number of files altered."""
    file_without_metadata = tmp_path / 'clean.png'
    file_without_metadata.touch()

    files_changed = cli.main([str(file_without_metadata), str(image_with_metadata)])

    assert files_changed == 1

    assert capsys.readouterr().out.strip().endswith(str(image_with_metadata))


def test_cli_version(capsys):
    """Confirm that --version works."""
    with pytest.raises(SystemExit):
        cli.main(['--version'])
    assert f'{cli.PROG} {cli.__version__}' == capsys.readouterr().out.strip()


@pytest.mark.parametrize(['flag', 'return_code'], [['--version', 0], ['', 1]])
def test_main_access_cli(flag, return_code, image_with_metadata):
    """Confirm that CLI can be accessed via python -m."""
    result = subprocess.run(
        [sys.executable, '-m', 'exif_stripper.cli', flag or str(image_with_metadata)]
    )
    assert result.returncode == return_code
