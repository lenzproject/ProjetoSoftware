import os

# A aplicação exige SECRET_KEY durante a importação da configuração.
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")

import pytest
from app import create_app


class TestConfig:
    TESTING = True
    SECRET_KEY = "test-secret-key-not-for-production"
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    DB_HOST = "127.0.0.1"
    DB_PORT = 3306
    DB_NAME = "fiscal_test"
    DB_USER = "test"
    DB_PASSWORD = "test"


@pytest.fixture
def app():
    return create_app(TestConfig)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def logged_client(client):
    with client.session_transaction() as session:
        session["user"] = {
            "id": 1,
            "email": "teste@example.com",
            "masterCNPJ": "12345678000199",
            "permission_register_product": "1",
            "permission_register_customer": "1",
            "permission_stock": "1",
            "permission_kardex": "1",
            "permission_reports": "1",
        }
        session["_csrf"] = "csrf-test-token"
    return client


@pytest.fixture
def csrf():
    return {"_csrf": "csrf-test-token"}
