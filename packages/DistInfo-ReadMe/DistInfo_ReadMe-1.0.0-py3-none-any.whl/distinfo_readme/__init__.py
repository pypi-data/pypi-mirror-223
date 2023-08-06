import sys, os
from importlib.metadata import distribution


if os.path.split(__path__[0])[0] in sys.path[1:]:
    __version__ = distribution(__name__).version
else:
    __version__ = '0.0.0'

from .main import post_view


__all__ = ['post_view']
