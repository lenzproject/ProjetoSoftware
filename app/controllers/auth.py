import secrets
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from mysql.connector import Error
from ..repositories.auth_repository import find_active_user, update_password
from ..utils.security import current_user, verify_password, hash_password

auth_bp=Blueprint("auth", __name__)

@auth_bp.get("/")
def login():
    if current_user(): return redirect(url_for("dashboard.index"))
    return render_template("login.html")

@auth_bp.post("/login")
def authenticate():
    login_value=request.form.get("email","").strip()
    password=request.form.get("password","")
    if not login_value or not password:
        flash("Informe usuário e senha.","warning")
        return redirect(url_for("auth.login"))
    try:
        user=find_active_user(login_value)
        valid, legacy=verify_password(password, (user or {}).get("password"))
        if not user or not valid:
            flash("Usuário ou senha inválidos.","danger")
            return redirect(url_for("auth.login"))
        if legacy:
            update_password(user["id"], hash_password(password))
        session.clear()
        session["user"]={k:v for k,v in user.items() if k!="password"}
        session["_csrf"]=secrets.token_urlsafe(32)
        session.permanent=True
        return redirect(url_for("dashboard.index"))
    except Error:
        current_app.logger.exception("Erro de autenticação")
        flash("Falha ao conectar ao banco. Confira as configurações.","danger")
        return redirect(url_for("auth.login"))

@auth_bp.post("/sair")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
