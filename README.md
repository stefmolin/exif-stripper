# exif-stripper
Pre-commit hook to ensure image EXIF data is removed.

## Usage
Add the following to your `.pre-commit-config.yaml` file:

```yaml
- repo: https://github.com/stefmolin/exif-stripper
  rev: 0.1.1
  hooks:
    - id: strip-exif
```
