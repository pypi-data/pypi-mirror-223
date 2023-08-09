# !/usr/bin/env python

from sanic import Sanic
from src.views import html_bp, json_bp, wechat_bp

app = Sanic(__name__)
app.blueprint(json_bp)
app.blueprint(html_bp)
app.blueprint(wechat_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
