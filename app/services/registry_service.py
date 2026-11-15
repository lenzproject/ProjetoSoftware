from ..models.registry import MODULES, LABELS
from ..repositories import registry_repository as repo

def module_config(module):
    if module not in MODULES:
        raise KeyError(module)
    return MODULES[module]

def form_fields(table, tenant):
    return [c for c in repo.get_columns(table)
            if c["Field"] not in ("id", tenant, "masterCNPJ")]

def collect_form_data(fields, form):
    data={}
    for col in fields:
        name=col["Field"]
        value=form.get(name, "").strip()
        data[name]=value if value != "" else None
    return data

def field_label(name):
    return LABELS.get(name, name.replace("_"," ").capitalize())
