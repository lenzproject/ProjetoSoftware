import decimal
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from mysql.connector import Error
from ..database import get_connection
from ..utils.security import login_required, current_user, require_permission

inventory_bp=Blueprint("inventory",__name__)

@inventory_bp.get("/estoque")
@login_required
def stock():
    require_permission("stock")
    conn=get_connection(); cur=conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT s.*,p.productdescription FROM stock s LEFT JOIN products p ON p.productcode=s.stockproductcode AND p.CNPJ=s.CNPJ WHERE s.CNPJ=%s ORDER BY p.productdescription",(current_user().get("masterCNPJ"),))
        return render_template("stock.html",rows=cur.fetchall())
    finally:
        cur.close(); conn.close()

@inventory_bp.post("/estoque/ajustar")
@login_required
def stock_adjust():
    require_permission("stock")
    try:
        code=request.form.get("code","").strip()
        kind=request.form.get("kind","E")
        qty=decimal.Decimal(request.form.get("qty","0").replace(",","."))
        unit=decimal.Decimal(request.form.get("unit","0").replace(",","."))
        description=request.form.get("description","Ajuste manual")[:120]
        if kind not in ("E","S") or not code or qty<=0 or unit<0:
            raise ValueError("Informe produto, operação, quantidade e valor válidos.")
        company=current_user().get("masterCNPJ")
        conn=get_connection(); cur=conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT id FROM products WHERE productcode=%s AND CNPJ=%s LIMIT 1",(code,company))
            if not cur.fetchone(): raise ValueError("Produto não encontrado nesta empresa.")
            cur.execute("SELECT * FROM stock WHERE stockproductcode=%s AND CNPJ=%s LIMIT 1 FOR UPDATE",(code,company))
            stock=cur.fetchone()
            if not stock:
                cur.execute("SELECT COALESCE(MAX(id),0)+1 n FROM stock"); sid=cur.fetchone()["n"]
                cur.execute("INSERT INTO stock (id,stockproductcode,stockproductphisic,stockproductreserved,stockproductavailable,stockunitvalue,CNPJ) VALUES (%s,%s,0,0,0,0,%s)",(sid,code,company))
                physical=decimal.Decimal("0"); reserved=decimal.Decimal("0")
            else:
                physical=decimal.Decimal(str(stock["stockproductphisic"] or 0))
                reserved=decimal.Decimal(str(stock["stockproductreserved"] or 0))
            new=physical+(qty if kind=="E" else -qty)
            if new<0: raise ValueError("Estoque insuficiente para esta saída.")
            old_unit=decimal.Decimal(str((stock or {}).get("stockunitvalue") or 0))
            average=unit if kind=="E" else old_unit
            if kind=="E" and new>0: average=((physical*old_unit)+(qty*unit))/new
            cur.execute("UPDATE stock SET stockproductphisic=%s,stockproductavailable=%s,stockunitvalue=%s WHERE stockproductcode=%s AND CNPJ=%s",(str(new),str(new-reserved),str(average),code,company))
            cur.execute("SELECT COALESCE(MAX(id),0)+1 n FROM kardex"); kid=cur.fetchone()["n"]
            cur.execute("""INSERT INTO kardex (id,kardexproductcode,kardexdatemodified,kardexoperationtype,kardexdescription,kardexinputamount,kardexinputvalue,kardexoutputamount,kardexoutputvalue,kardexbalance,kardexunitbalance,kardexbalancevalue,CNPJ)
                VALUES (%s,%s,NOW(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (kid,code,kind,description,str(qty if kind=="E" else 0),str(qty*unit if kind=="E" else 0),str(qty if kind=="S" else 0),str(qty*unit if kind=="S" else 0),str(new),str(average),str(new*average),company))
            conn.commit()
            flash("Movimentação registrada e Kardex atualizado.","success")
        except Exception:
            conn.rollback(); raise
        finally:
            cur.close(); conn.close()
    except (Error,ValueError,decimal.InvalidOperation):
        current_app.logger.exception("Falha no ajuste de estoque")
        flash("Não foi possível registrar a movimentação. Confira os dados e o estoque disponível.","danger")
    return redirect(url_for("inventory.stock"))

@inventory_bp.get("/kardex")
@login_required
def kardex():
    require_permission("kardex")
    conn=get_connection(); cur=conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM kardex WHERE CNPJ=%s ORDER BY kardexdatemodified DESC,id DESC LIMIT 1000",(current_user().get("masterCNPJ"),))
        return render_template("kardex.html",rows=cur.fetchall())
    finally:
        cur.close(); conn.close()
