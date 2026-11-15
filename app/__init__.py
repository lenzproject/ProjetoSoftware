from flask import Flask
from .config import Config
from .controllers.auth import auth_bp
from .controllers.dashboard import dashboard_bp
from .controllers.registry import registry_bp
from .controllers.inventory import inventory_bp
from .controllers.operations import operations_bp
from .utils.security import csrf_token, permitted, validate_csrf
from .models.registry import MODULES, LABELS

def create_app(config_class=Config):
    app = Flask(__name__, template_folder="templates", static_folder="../static")
    app.config.from_object(config_class)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(registry_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(operations_bp)

    app.before_request(validate_csrf)

    @app.context_processor
    def inject_globals():
        return {"csrf_token": csrf_token, "permitted": permitted,
                "modules": MODULES, "labels": LABELS}

    @app.errorhandler(403)
    def forbidden(error):
        from flask import render_template
        return render_template("error.html", code=403,
            message="Você não possui permissão para acessar este recurso."), 403

    @app.errorhandler(404)
    def not_found(error):
        from flask import render_template
        return render_template("error.html", code=404,
            message="Página ou registro não encontrado."), 404

    @app.errorhandler(400)
    def bad_request(error):
        from flask import render_template
        return render_template("error.html", code=400,
            message=getattr(error, "description", "Solicitação inválida.")), 400
    return app
