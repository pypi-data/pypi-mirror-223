# jupyter_sentry_extension


Sentry extension for Jupyter Server. \
`SENTRY_JUPYTER_SERVER_DSN` environment variable should be defined to 

## Install

To install the extension, execute:

```bash
pip install jupyter_sentry_extension
```

### Sentry DSN

To capture errors on Jupyter Server you should provide DSN in `SENTRY_JUPYTER_SERVER_DSN` environment variable.

## Uninstall

To remove the extension, execute:

```bash
pip uninstall jupyter_sentry_extension
```

## Troubleshoot

If you are seeing the frontend extension, but it is not working, check
that the server extension is enabled:

```bash
jupyter server extension list
```

### Packaging the extension

See [RELEASE](RELEASE.md)
