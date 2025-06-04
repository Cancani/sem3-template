from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)

admin_bp = Blueprint('admin', __name__)

# Dummy user
USERS = {
    "admin": "password123"
}

@admin_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user_pass = USERS.get(username)
    if not user_pass or user_pass != password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@admin_bp.route('/devices', methods=['POST'])
@jwt_required()
def add_device():
    current_user = get_jwt_identity()
    data = request.json
    # Beispiel: Gerät hinzufügen (hier einfach Bestätigung)
    name = data.get('name')
    if not name:
        return jsonify({"msg": "Missing device name"}), 400

    # TODO: Geräte in Device-Liste oder DB speichern

    return jsonify({"msg": f"Device '{name}' added by {current_user}"}), 201
