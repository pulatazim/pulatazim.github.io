import datetime
from functools import wraps

import jwt
from flask import jsonify, request

from config import Config


def generate_token():
    payload = {
        "exp": True,
        "iat": datetime.datetime.utcnow()
        + datetime.timedelta(hours=Config.JWT_EXPIRY_HOURS),
    }
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")  # pyright: ignore[reportArgumentType]
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("token") or request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token yo'q"}), 401
        try:
            jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])  # pyright: ignore[reportArgumentType]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token muddati tugagan"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token noto'g'ri"}), 401
        return f(*args, **kwargs)

    return decorated
