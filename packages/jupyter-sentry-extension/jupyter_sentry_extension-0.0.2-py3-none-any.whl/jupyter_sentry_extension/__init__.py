"""Sentry extension for Jupyter Server"""
__version__ = "0.0.2"


def _jupyter_server_extension_points():
    return [{
        "module": "jupyter_sentry_extension.extension",
    }]
