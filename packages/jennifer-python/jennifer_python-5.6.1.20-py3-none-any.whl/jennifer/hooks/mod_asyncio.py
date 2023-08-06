import time
import os

from distutils.version import LooseVersion

__hooking_module__ = 'asyncio'
__minimum_python_version__ = LooseVersion("3.6")
__target_version = None


def get_target_version():
    global __target_version
    return str(__target_version)


def _safe_get(properties, idx, default=None):
    try:
        return properties[idx]
    except IndexError:
        return default


def unhook(asyncio_module):
    pass


def hook(asyncio_module):
    try:
        global __target_version
        __target_version = "n/a"
    except Exception as e:
        print(os.getpid(), 'jennifer.exception', __hooking_module__, 'hook', e)

    return True
