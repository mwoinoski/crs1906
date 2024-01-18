from pkg_resources import get_distribution, DistributionNotFound

__project__ = 'setup_example'
__version__ = None  # required for initial installation

try:
    # load version number from value passed to setup.py's setup()
    __version__ = get_distribution(__project__).version
except DistributionNotFound:  # package is not installed
    __version__ = __project__ + '-(local)'
