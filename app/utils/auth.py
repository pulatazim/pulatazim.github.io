import datetime
from functools import wraps

import jwt
from flask import redirect, request

from config import Config


def generate_token():
    payload = {
        "admin": True,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(hours=Config.JWT_EXPIRY_HOURS),
    }
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")  # pyright: ignore[reportArgumentType]
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("token")

        if not token:
            return redirect("/admin/login")
        try:
            jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])  # pyright: ignore[reportArgumentType]
        except jwt.ExpiredSignatureError:
            return redirect("/admin/login")
        except jwt.InvalidTokenError:
            return redirect("/admin/login")
        return f(*args, **kwargs)

    return decorated
