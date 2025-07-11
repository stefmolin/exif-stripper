"""Common test fixtures."""

import pytest
from PIL import ExifTags, Image


@pytest.fixture
def image_without_exif_data(tmp_path):
    """Fixture for an image without EXIF data."""
    image_without_exif_data = tmp_path / 'clean.png'
    image_without_exif_data.touch()
    return image_without_exif_data


@pytest.fixture
def image_with_exif_data(tmp_path):
    """Fixture for an image with only the required EXIF data."""
    image_file = tmp_path / 'test.png'
    with Image.new(mode='1', size=(2, 2)) as im:
        exif = im.getexif()

        exif[ExifTags.Base.InterColorProfile] = 'some color profile'
        exif[ExifTags.Base.Orientation] = 1

        im.save(image_file, exif=exif)

    return image_file


@pytest.fixture
def image_with_full_exif_data(image_with_exif_data):
    """Fixture for an image with EXIF data."""
    with Image.open(image_with_exif_data) as im:
        exif = im.getexif()

        exif[ExifTags.Base.CameraOwnerName] = 'Unknown'

        exif[ExifTags.Base.Artist] = 'Stefanie Molin'
        exif[ExifTags.Base.Copyright] = 'Copyright (c) Stefanie Molin.'

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

        im.save(image_with_exif_data, exif=exif)

    return image_with_exif_data
