from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes.devices import devices_bp
    app.register_blueprint(devices_bp, url_prefix='/api/devices')

    return app
