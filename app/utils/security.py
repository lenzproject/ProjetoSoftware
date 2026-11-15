import base64, hashlib, secrets
from functools import wraps
from flask import session, request, redirect, url_for, abort
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.registry import PERMISSIONS

def current_user():
    return session.get("user")

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped

def permitted(key):
    user = current_user() or {}
    field = PERMISSIONS.get(key)
    return bool(field and str(user.get(field, "0")) == "1")

def require_permission(key):
    if not permitted(key):
        abort(403)

def csrf_token():
    token = session.get("_csrf")
    if not token:
        token = secrets.token_urlsafe(32)
        session["_csrf"] = token
    return token

def validate_csrf():
    if request.method == "POST" and request.endpoint != "static":
        if not secrets.compare_digest(request.form.get("_csrf", ""), session.get("_csrf", "")):
            abort(400, "Token de segurança inválido. Atualize a página.")

def verify_password(password, stored):
    if not stored:
        return False, False
    try:
        if check_password_hash(stored, password):
            return True, False
    except (ValueError, TypeError):
        pass
    legacy = base64.b64encode(hashlib.sha1(password.encode("utf-8")).digest()).decode("ascii")
    return secrets.compare_digest(legacy, stored), True

def hash_password(password):
    return generate_password_hash(password)
