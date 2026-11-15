from werkzeug.security import generate_password_hash


def test_dashboard_redirects_when_not_authenticated(client):
    response = client.get("/painel")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_dashboard_is_available_after_login(logged_client):
    response = logged_client.get("/painel")
    assert response.status_code == 200
    assert b"teste@example.com" in response.data


def test_post_without_csrf_is_rejected(logged_client):
    response = logged_client.post("/sair", data={})
    assert response.status_code == 400


def test_logout_clears_session(logged_client, csrf):
    response = logged_client.post("/sair", data=csrf)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
    with logged_client.session_transaction() as session:
        assert "user" not in session


def test_login_authenticates_and_does_not_store_password_in_session(
    client, monkeypatch
):
    from app.controllers import auth
    user = {
        "id": 7,
        "email": "ana@example.com",
        "password": generate_password_hash("Senha123"),
        "active": 1,
        "masterCNPJ": "12345678000199",
    }
    monkeypatch.setattr(auth, "find_active_user", lambda login: user if login == user["email"] else None)
    with client.session_transaction() as session:
        session["_csrf"] = "login-token"
    response = client.post("/login", data={
        "_csrf": "login-token", "email": "ana@example.com", "password": "Senha123"
    })
    assert response.status_code == 302
    with client.session_transaction() as session:
        assert session["user"]["email"] == "ana@example.com"
        assert "password" not in session["user"]


def test_login_rejects_invalid_password(client, monkeypatch):
    from app.controllers import auth
    monkeypatch.setattr(auth, "find_active_user", lambda login: {
        "id": 1, "email": login, "password": generate_password_hash("correta")
    })
    with client.session_transaction() as session:
        session["_csrf"] = "login-token"
    response = client.post("/login", data={
        "_csrf": "login-token", "email": "x@example.com", "password": "errada"
    })
    assert response.status_code == 302
    with client.session_transaction() as session:
        assert "user" not in session


def test_registry_list_uses_company_scope(logged_client, monkeypatch):
    from app.controllers import registry
    captured = {}
    def fake_list(table, tenant, company):
        captured.update(table=table, tenant=tenant, company=company)
        return []
    monkeypatch.setattr(registry.repo, "list_records", fake_list)
    response = logged_client.get("/cadastros/products")
    assert response.status_code == 200
    assert captured == {
        "table": "products", "tenant": "CNPJ", "company": "12345678000199"
    }


def test_registry_unknown_module_returns_404(logged_client):
    response = logged_client.get("/cadastros/modulo-invalido")
    assert response.status_code == 404


def test_registry_requires_module_permission(client):
    with client.session_transaction() as session:
        session["user"] = {"masterCNPJ": "123", "permission_register_product": "0"}
    response = client.get("/cadastros/products")
    assert response.status_code == 403


def test_registry_create_post_calls_repository(logged_client, csrf, monkeypatch):
    from app.controllers import registry
    monkeypatch.setattr(registry, "form_fields", lambda table, tenant: [
        {"Field": "productcode"}, {"Field": "productdescription"}
    ])
    captured = {}
    monkeypatch.setattr(registry.repo, "get_record", lambda *args: None)
    def fake_save(table, tenant, company, data, row_id=None):
        captured.update(table=table, tenant=tenant, company=company, data=data, row_id=row_id)
    monkeypatch.setattr(registry.repo, "save_record", fake_save)
    response = logged_client.post("/cadastros/products/novo", data={
        **csrf, "productcode": " P001 ", "productdescription": " Produto teste "
    })
    assert response.status_code == 302
    assert captured["table"] == "products"
    assert captured["company"] == "12345678000199"
    assert captured["data"] == {"productcode": "P001", "productdescription": "Produto teste"}
