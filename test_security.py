import base64
import hashlib

from werkzeug.security import generate_password_hash

from app.utils.security import verify_password, hash_password, permitted


def test_verify_password_werkzeug_hash():
    stored = generate_password_hash("SenhaForte123")
    assert verify_password("SenhaForte123", stored) == (True, False)
    assert verify_password("incorreta", stored) == (False, True)


def test_verify_password_legacy_sha1_base64():
    digest = hashlib.sha1("senha-legada".encode("utf-8")).digest()
    stored = base64.b64encode(digest).decode("ascii")
    assert verify_password("senha-legada", stored) == (True, True)
    assert verify_password("outra", stored) == (False, True)


def test_verify_password_without_stored_value():
    assert verify_password("qualquer", None) == (False, False)
    assert verify_password("qualquer", "") == (False, False)


def test_hash_password_generates_usable_hash():
    stored = hash_password("abc123")
    assert stored != "abc123"
    assert verify_password("abc123", stored) == (True, False)


def test_permitted_requires_explicit_string_one(app):
    from flask import session
    with app.test_request_context("/"):
        session["user"] = {"permission_register_product": "1"}
        assert permitted("products") is True
        session["user"]["permission_register_product"] = "0"
        assert permitted("products") is False
        assert permitted("modulo_inexistente") is False
