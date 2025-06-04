from flask import Flask
from flask_jwt_extended import JWTManager
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt = JWTManager(app)

    from app.routes.devices import devices_bp
    app.register_blueprint(devices_bp, url_prefix='/api/devices')

    from app.routes.history import history_bp
    app.register_blueprint(history_bp, url_prefix='/api/history')

    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    return app
