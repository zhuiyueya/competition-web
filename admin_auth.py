import os
from functools import wraps

from flask import request, jsonify, current_app
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from werkzeug.security import check_password_hash


def _serializer(secret_key: str) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(secret_key=secret_key, salt="admin-auth")


def create_admin_token(payload: dict) -> str:
    s = _serializer(current_app.config["SECRET_KEY"])
    return s.dumps(payload)


def verify_admin_token(token: str, max_age_seconds: int) -> dict | None:
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


def require_admin(max_age_seconds: int = 12 * 60 * 60):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            token = _extract_bearer_token()
            payload = verify_admin_token(token, max_age_seconds=max_age_seconds)
            if not payload or payload.get("role") != "admin":
                return jsonify({"success": False, "message": "未登录或登录已过期"}), 401
            request.admin_payload = payload
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def verify_admin_credentials(username: str, password: str) -> bool:
    env_user = os.environ.get("ADMIN_USERNAME", "admin")
    if username != env_user:
        return False

    pwd_hash = os.environ.get("ADMIN_PASSWORD_HASH")
    if pwd_hash:
        try:
            return check_password_hash(pwd_hash, password)
        except Exception:
            return False

    env_pwd = os.environ.get("ADMIN_PASSWORD")
    if env_pwd is None:
        return False
    return password == env_pwd
