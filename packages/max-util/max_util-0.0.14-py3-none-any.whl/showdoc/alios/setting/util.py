import os
import platform
__window = 'Windows'
__linux = 'Linux'


def platform_get():
    return platform.system()


def user_location_get():
    if __window == platform_get():
        return os.getenv("USERPROFILE")
    elif __linux == platform_get():
        return os.path.expanduser("~")
    else:
        OSError('un know os')
