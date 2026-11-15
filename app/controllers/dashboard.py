from flask import Blueprint, render_template
from ..utils.security import login_required, current_user, require_permission
from ..database import get_connection

dashboard_bp=Blueprint("dashboard",__name__)

@dashboard_bp.get("/painel")
@login_required
def index():
    return render_template("dashboard.html",user=current_user())

@dashboard_bp.get("/relatorios")
@login_required
def reports():
    require_permission("reports")
    conn=get_connection(); cur=conn.cursor(dictionary=True); company=current_user().get("masterCNPJ")
    try:
        cur.execute("SELECT COUNT(*) total, COALESCE(SUM(stockproductphisic),0) units FROM stock WHERE CNPJ=%s",(company,))
        stock_summary=cur.fetchone()
        cur.execute("SELECT COUNT(*) total FROM products WHERE CNPJ=%s",(company,)); products_count=cur.fetchone()["total"]
        cur.execute("SELECT COUNT(*) total FROM customers WHERE CNPJ=%s",(company,)); customers_count=cur.fetchone()["total"]
        return render_template("reports.html",stock_summary=stock_summary,products_count=products_count,customers_count=customers_count)
    finally:
        cur.close(); conn.close()
