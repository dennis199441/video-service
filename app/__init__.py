from flask import Flask


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    
    with app.app_context():
        # Imports
        from .api.process import process
        from .api.ptype import ptype

        # REGISTER ROUTES
        app.register_blueprint(process, url_prefix="/process")
        app.register_blueprint(ptype, url_prefix="/ptype")

        return app