from functools import wraps

from sanic import Sanic
from sanic.response import html, json, text

app = Sanic(__name__)

session_dict = {}


def check_request_for_authorization_status(request):
    session = session_dict.get("test")
    cookie = request.cookies.get("test")
    print("aaa", session, cookie)
    if session and cookie:
        flag = True
    else:
        flag = False
    return flag


def authorized(f):
    @wraps(f)
    async def decorated_function(request, *args, **kwargs):
        # run some method that checks the request
        # for the client's authorization status
        is_authorized = check_request_for_authorization_status(request)

        if is_authorized:
            # the user is authorized.
            # run the handler method and return the response
            response = await f(request, *args, **kwargs)
            return response
        else:
            # the user is not authorized.
            return json({"status": "not_authorized"}, 403)

    return decorated_function


@app.route("/")
@authorized
async def test(request):
    return json({"status": "authorized"})


@app.route("/auth")
async def test1(request):
    session_dict["aaa"] = "bbb"
    response = text("auth")
    response.cookies["test"] = "It worked!"
    response.cookies["test"]["max-age"] = 10
    session_dict["test"] = "It worked!"
    return response


@app.route("/login")
async def login(request):
    return html("login")


@app.route("/logout")
async def logout(request):
    url = app.url_for("login")
    print(url)
    session_dict.pop("test", 0)
    return html("login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8004)
