from functools import wraps

from flask import request, jsonify, current_app
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


def _serializer(secret_key: str) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(secret_key=secret_key, salt="user-auth")


def create_user_token(payload: dict) -> str:
    s = _serializer(current_app.config["SECRET_KEY"])
    return s.dumps(payload)


def verify_user_token(token: str, max_age_seconds: int) -> dict | None:
    if not token:
        return None
    s = _serializer(current_app.config["SECRET_KEY"])
    try:
        return s.loads(token, max_age=max_age_seconds)
    except (BadSignature, SignatureExpired):
        return None


def _extract_bearer_token() -> str:
    auth = request.headers.get("Authorization", "")
    if not auth:
        return ""
    parts = auth.split(" ", 1)
    if len(parts) != 2:
        return ""
    scheme, token = parts[0].strip(), parts[1].strip()
    if scheme.lower() != "bearer":
        return ""
    return token


def require_user(max_age_seconds: int = 30 * 24 * 60 * 60):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            token = _extract_bearer_token()
            payload = verify_user_token(token, max_age_seconds=max_age_seconds)
            if not payload or payload.get("role") != "user":
                return jsonify({"success": False, "message": "未登录或登录已过期"}), 401
            request.user_payload = payload
            return fn(*args, **kwargs)

        return wrapper

    return decorator
