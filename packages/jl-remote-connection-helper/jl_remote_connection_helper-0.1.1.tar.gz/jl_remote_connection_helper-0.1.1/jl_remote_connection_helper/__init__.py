from jupyter_server.serverapp import ServerApp

try:
    from ._version import __version__
except ImportError:
    # Fallback when using the package in dev mode without installing
    # in editable mode with pip. It is highly recommended to install
    # the package from a stable release or in editable mode: https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
    import warnings
    warnings.warn("Importing 'jl_remote_connection_helper' outside a proper installation.")
    __version__ = "dev"
from .handlers import setup_handlers


def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": "jl-remote-connection-helper"
    }]


def _jupyter_server_extension_points():
    return [{
        "module": "jl_remote_connection_helper"
    }]


def _load_jupyter_server_extension(server_app: ServerApp) -> None:
    """Registers the API handler to receive HTTP requests from the frontend extension.

    Parameters
    ----------
    server_app: jupyter_server.serverapp.ServerApp
        Jupyter Server application instance
    """
    setup_handlers(server_app.web_app)
    name = "jl_remote_connection_helper"
    server_app.log.info(f"Registered {name} server extension")
