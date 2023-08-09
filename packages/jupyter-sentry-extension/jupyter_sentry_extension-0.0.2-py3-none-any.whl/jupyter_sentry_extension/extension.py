import os

import sentry_sdk
from sentry_sdk.integrations.tornado import TornadoIntegration

from jupyter_server.serverapp import ServerApp


def _load_jupyter_server_extension(serverapp: ServerApp):
    """
    This function is called when the extension is loaded.
    """
    _SENTRY_JUPYTER_SERVER_DSN = os.getenv("SENTRY_JUPYTER_SERVER_DSN")

    if _SENTRY_JUPYTER_SERVER_DSN:
        sentry_sdk.init(
            dsn=_SENTRY_JUPYTER_SERVER_DSN,
            integrations=[TornadoIntegration()],
            traces_sample_rate=1.0,
        )
        serverapp.log.info("Sentry configured!")
    else:
        serverapp.log.info("Sentry is not configured:(")
