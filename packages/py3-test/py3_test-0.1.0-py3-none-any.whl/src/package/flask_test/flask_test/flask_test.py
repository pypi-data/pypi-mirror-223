"""
@author: lijc210@163.com
@file: flask_test.py
@time: 2020/06/08
@desc: 功能描述。
"""

from flask import Flask, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def hello_world():
    # return 'Hello, World!'
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
