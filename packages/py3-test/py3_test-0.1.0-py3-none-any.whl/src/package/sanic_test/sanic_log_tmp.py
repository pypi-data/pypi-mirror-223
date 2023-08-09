"""
@Time   : 2019/2/26
@author : lijc210@163.com
@Desc:  : 功能描述。
"""
import sys
import time

from sanic import Sanic
from sanic.response import json

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "sanic.root": {"level": "INFO", "handlers": ["console"]},
        "sanic.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "propagate": True,
            "qualname": "sanic.error",
        },
        "sanic.access": {
            "level": "INFO",
            "handlers": ["access_console", "access_file"],
            "propagate": True,
            "qualname": "sanic.access",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout,
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stderr,
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": sys.stdout,
        },
        "access_file": {
            "class": "logging.FileHandler",
            "formatter": "access",
            "filename": "log.log",
        },
    },
    "formatters": {
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
        "access": {
            "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: "
            + "%(request)s %(message)s %(status)d %(byte)d",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
    },
}

app = Sanic(log_config=LOGGING)


@app.middleware("request")
async def add_start_time(request):
    request["start_time"] = time.time()


@app.middleware("response")
async def add_spent_time(request, response):
    request["spent_time"] = time.time() - request["start_time"]


@app.route("/", methods=["POST"])
async def test(request):
    print(request.url)
    print(request.body)
    return json({"hello": "world"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
