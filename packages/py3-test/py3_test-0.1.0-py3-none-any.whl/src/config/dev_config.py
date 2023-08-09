#!/usr/bin/env python
from .config import Config


class DevConfig(Config):
    # Application config
    MODE = "dev"
    DEBUG = True
    ES_HOST = ""
    SNIFF_ON_START = False
