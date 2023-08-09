#!/usr/bin/env python
from .config import Config


class ProConfig(Config):
    # Application config
    MODE = "prod"
    DEBUG = False
    ES_HOST = ""
    SNIFF_ON_START = False
