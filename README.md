# exif-stripper

Pre-commit hook to ensure image metadata (EXIF data and extended attributes) is removed.

<table>
   <tr>
     <td>
      <img alt="Last Release" src="https://img.shields.io/badge/last%20release-inactive?style=for-the-badge">
     </td>
     <td>
      <a href="https://pypi.org/project/exif-stripper/" target="_blank" rel="noopener noreferrer">
        <img alt="PyPI release" src="https://img.shields.io/pypi/v/exif-stripper.svg">
      </a>
      <a href="https://pypi.org/project/exif-stripper/" target="_blank" rel="noopener noreferrer">
        <img alt="Supported Python Versions" src="https://img.shields.io/pypi/pyversions/exif-stripper">
      </a>
      <a href="https://github.com/stefmolin/exif-stripper/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">
         <img alt="License" src="https://img.shields.io/pypi/l/exif-stripper.svg?color=blueviolet">
      </a>
     </td>
   </tr>
   <tr>
     <td>
      <img alt="Build status" src="https://img.shields.io/badge/build%20status-inactive?style=for-the-badge">
     </td>
     <td>
      <a href="https://codecov.io/gh/stefmolin/exif-stripper" target="_blank" rel="noopener noreferrer">
        <img alt="codecov" src="https://codecov.io/gh/stefmolin/exif-stripper/branch/main/graph/badge.svg?token=3SEEG9SZQO">
      </a>
      <a href="https://github.com/stefmolin/exif-stripper/actions/workflows/ci.yml" target="_blank" rel="noopener noreferrer">
        <img alt="CI" src="https://github.com/stefmolin/exif-stripper/actions/workflows/ci.yml/badge.svg">
      </a>
     </td>
   </tr>
   <tr>
     <td>
      <img alt="Downloads" src="https://img.shields.io/badge/%23downloads-inactive?style=for-the-badge">
     </td>
     <td>
      <a href="https://pypi.org/project/exif-stripper/" target="_blank" rel="noopener noreferrer">
        <img alt="PyPI downloads" src="https://img.shields.io/pepy/dt/exif-stripper?label=pypi&color=blueviolet">
      </a>
     </td>
   </tr>
  </table>

## Usage

### Pre-commit hook

Add the following to your `.pre-commit-config.yaml` file:

```yaml
- repo: https://github.com/stefmolin/exif-stripper
  rev: 0.4.0
  hooks:
    - id: strip-exif
```

Be sure to check out the [pre-commit documentation](https://pre-commit.com/#pre-commit-configyaml---hooks) for additional configuration options.

### Command line

First, install the `exif-stripper` package from PyPI:

```shell
$ python -m pip install exif-stripper
```

Then, use the `strip-exif` entry point on the file(s) of your choice:

```shell
$ strip-exif /path/to/file [/path/to/another/file]
```

Run `strip-exif --help` for more information.

### Python

First, install the `exif-stripper` package from PyPI:

```shell
$ python -m pip install exif-stripper
```

Then, use the `process_image()` function on individual files (returns `True` if the file was altered and `False` otherwise):

```python
from exif_stripper import process_image
process_image('/path/to/image')
```

*Note: This requires version 0.4.0 or above.*

## Contributing

Please consult the [contributing guidelines](CONTRIBUTING.md).
