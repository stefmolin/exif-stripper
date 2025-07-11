"""Test the CLI."""

import subprocess
import sys

import pytest

from exif_stripper import cli
from exif_stripper.fields import FieldGroup

from .common import has_expected_metadata


@pytest.mark.parametrize(
    ('fields', 'preserve_copyright'),
    [
        (None, None),
        ([FieldGroup.ALL], True),
        ([FieldGroup.ALL, FieldGroup.GPS], False),
        ([FieldGroup.GPS], True),
        ([FieldGroup.CAMERA, FieldGroup.LENS, FieldGroup.SERIALS], None),
    ],
)
def test_main(
    capsys,
    image_without_exif_data,
    image_with_full_exif_data,
    fields,
    preserve_copyright,
):
    """Test that cli.main() returns the number of files altered."""
    cli_args = [str(image_without_exif_data), str(image_with_full_exif_data)]
    if fields is not None:
        cli_args = ['--fields', *[str(field) for field in fields], '--', *cli_args]
    if preserve_copyright is False:
        cli_args = ['--remove-copyright', *cli_args]

    files_changed = cli.main(cli_args)

    assert files_changed == 1
    assert has_expected_metadata(
        image_with_full_exif_data,
        fields,
        has_copyright=preserve_copyright is not False,
        was_stripped=True,
    )

    assert capsys.readouterr().out.strip().endswith(str(image_with_full_exif_data))


def test_cli_version(capsys):
    """Confirm that --version works."""
    with pytest.raises(SystemExit):
        cli.main(['--version'])
    assert f'{cli.PROG} {cli.__version__}' == capsys.readouterr().out.strip()


@pytest.mark.parametrize(('flag', 'return_code'), [('--version', 0), ('', 1)])
def test_main_access_cli(flag, return_code, image_with_full_exif_data):
    """Confirm that CLI can be accessed via python -m."""
    result = subprocess.run(
        [
            sys.executable,
            '-m',
            'exif_stripper.cli',
            flag or str(image_with_full_exif_data),
        ]
    )
    assert result.returncode == return_code


def test_cli_fields(capsys, image_with_full_exif_data):
    """Confirm that copyright isn't allowed as a field to remove on its own via the CLI."""
    with pytest.raises(SystemExit, match='2'):
        cli.main(['--fields', 'copyright', str(image_with_full_exif_data)])
    assert 'invalid choice' in capsys.readouterr().err.strip()
