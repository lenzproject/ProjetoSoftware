from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from mysql.connector import Error
from ..utils.security import login_required, current_user, require_permission
from ..services.registry_service import module_config, form_fields, collect_form_data
from ..repositories import registry_repository as repo

registry_bp=Blueprint("registry",__name__)

@registry_bp.get("/cadastros/<module>")
@login_required
def index(module):
    try: title,table,tenant,permission,display,secondary=module_config(module)
    except KeyError: abort(404)
    require_permission(module)
    rows=repo.list_records(table,tenant,current_user().get("masterCNPJ"))
    return render_template("registry.html",module=module,title=title,rows=rows,display=display,secondary=secondary)

@registry_bp.route("/cadastros/<module>/novo",methods=["GET","POST"])
@registry_bp.route("/cadastros/<module>/<int:row_id>/editar",methods=["GET","POST"])
@login_required
def form(module,row_id=None):
    try: title,table,tenant,permission,display,secondary=module_config(module)
    except KeyError: abort(404)
    require_permission(module)
    fields=form_fields(table,tenant)
    company=current_user().get("masterCNPJ")
    item=repo.get_record(table,tenant,company,row_id) if row_id is not None else None
    if row_id is not None and item is None: abort(404)
    if request.method=="POST":
        data=collect_form_data(fields,request.form)
        try:
            repo.save_record(table,tenant,company,data,row_id)
            flash("Registro salvo com sucesso.","success")
            return redirect(url_for("registry.index",module=module))
        except (Error,ValueError,LookupError):
            current_app.logger.exception("Falha ao salvar cadastro")
            flash("Não foi possível salvar. Verifique os dados informados e a estrutura do banco.","danger")
    return render_template("registry_form.html",module=module,title=title,fields=fields,item=item)

@registry_bp.post("/cadastros/<module>/<int:row_id>/excluir")
@login_required
def delete(module,row_id):
    try: title,table,tenant,*_=module_config(module)
    except KeyError: abort(404)
    require_permission(module)
    try:
        repo.delete_record(table,tenant,current_user().get("masterCNPJ"),row_id)
        flash("Registro excluído com sucesso.","success")
    except (Error,ValueError,LookupError) as exc:
        flash(str(exc) if isinstance(exc,(ValueError,LookupError)) else "Não foi possível excluir o registro.","danger")
    return redirect(url_for("registry.index",module=module))
