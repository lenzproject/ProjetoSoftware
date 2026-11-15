from flask import Blueprint, render_template, abort
from ..models.registry import READONLY_MODULES
from ..database import get_connection
from ..utils.security import login_required, current_user, require_permission

operations_bp=Blueprint("operations",__name__)

@operations_bp.get("/operacao/<module>")
@login_required
def listing(module):
    if module not in READONLY_MODULES: abort(404)
    title,table,permission=READONLY_MODULES[module]
    require_permission(module)
    conn=get_connection(); cur=conn.cursor(dictionary=True)
    try:
        cur.execute(f"SELECT * FROM `{table}` WHERE CNPJ=%s ORDER BY 1 DESC LIMIT 500",(current_user().get("masterCNPJ"),))
        rows=cur.fetchall()
        return render_template("readonly.html",title=title,rows=rows,module=module)
    finally:
        cur.close(); conn.close()
