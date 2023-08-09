#!/usr/bin/env python
import os
import socket
import sys
from platform import uname

from .dev_config import DevConfig
from .pro_config import ProConfig
from .test_config import TestConfig

UNDER_WINDOWS = sys.platform == "win32"
UNDER_MACOS = sys.platform == "darwin"
HOSTNAME = socket.gethostname()


def load_config():
    """
    Load a config class
    """

    MODE = os.environ.get("ENV", "prod")
    try:
        if (
            UNDER_WINDOWS
            or UNDER_MACOS
            or "dev" in HOSTNAME
            or "microsoft-standard" in uname().release
        ):
            MODE = "dev"
        if "test" in HOSTNAME:
            MODE = "test"
        print("环境初始化: load %s" % MODE)

        if MODE == "prod":
            return ProConfig
        elif MODE == "dev":
            return DevConfig
        elif MODE == "test":
            return TestConfig
        else:
            return DevConfig

    except ImportError:
        from .config import Config

        return Config


CONFIG = load_config()
