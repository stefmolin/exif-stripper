"""EXIF stripper."""

import importlib.metadata

from .fields import FieldGroup
from .processing import process_image

__version__ = importlib.metadata.version(__name__)

__all__ = ['FieldGroup', '__version__', 'process_image']
