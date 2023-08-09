# Making a new release of jupyter_sentry_extension

The extension can be published to `PyPI` manually

## Manual release

### Python package

This extension can be distributed as Python
packages. All of the Python
packaging instructions in the `pyproject.toml` file to wrap your extension in a
Python package. Before generating a package, we first need to install `build`.

```bash
pip install build twine
```

To create a Python source package (`.tar.gz`) and the binary package (`.whl`) in the `dist/` directory, do:

```bash
python -m build
```
> **NOTE**: Don't forget change version in `jupyter_server_extension/__init__.py` file before building!

> `python setup.py sdist bdist_wheel` is deprecated and will not work for this package.

Then to upload the package to PyPI, do:

```bash
twine upload dist/*
```