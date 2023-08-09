# !/usr/bin/env python
from multiprocessing import Process, freeze_support

from sanic import Sanic
from src.views import index_bp, wechat_bp
from src.views.network_weixin2 import main

app = Sanic(__name__)
app.blueprint(index_bp)
app.blueprint(wechat_bp)

if __name__ == "__main__":
    freeze_support()
    p = Process(target=main)
    p.start()  # 让这个进程开始执行test函数里面的代码
    # p.join()     #等进程p结束之后，才会继续向下走
    app.run(host="127.0.0.1", port=8000, workers=1)
