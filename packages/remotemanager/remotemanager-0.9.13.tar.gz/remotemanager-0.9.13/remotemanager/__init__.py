from .dataset.dataset import Dataset
from .connection.url import URL
from .logging.log import Handler
from .storage.remotefunction import RemoteFunction

__all__ = ["Dataset", "URL", "RemoteFunction"]  # noqa: F405
__version__ = "0.9.13"

# attach a global Logger to the manager
Logger = Handler()  # noqa: F405


# ipython magic
def load_ipython_extension(ipython):
    from remotemanager.jupyter.magic import RCell

    ipython.register_magics(RCell)
