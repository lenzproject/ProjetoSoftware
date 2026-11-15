import pytest

from app.services.registry_service import (
    module_config, form_fields, collect_form_data, field_label
)


def test_module_config_returns_known_module():
    config = module_config("products")
    assert config[0] == "Produtos"
    assert config[1] == "products"


def test_module_config_rejects_unknown_module():
    with pytest.raises(KeyError):
        module_config("nao_existe")


def test_form_fields_excludes_identity_and_tenant(monkeypatch):
    monkeypatch.setattr("app.services.registry_service.repo.get_columns", lambda table: [
        {"Field": "id"}, {"Field": "CNPJ"}, {"Field": "masterCNPJ"},
        {"Field": "productcode"}, {"Field": "productdescription"},
    ])
    assert [c["Field"] for c in form_fields("products", "CNPJ")] == [
        "productcode", "productdescription"
    ]


def test_collect_form_data_trims_and_converts_empty_to_none():
    fields = [{"Field": "name"}, {"Field": "email"}, {"Field": "notes"}]
    data = collect_form_data(fields, {"name": "  Produto  ", "email": "", "notes": " x "})
    assert data == {"name": "Produto", "email": None, "notes": "x"}


def test_field_label_uses_dictionary_then_fallback():
    assert field_label("productcode") == "Código"
    assert field_label("campo_novo") == "Campo novo"
