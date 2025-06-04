from flask import Blueprint, render_template, request, jsonify, abort
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from app.routes.devices import devices
from app.routes.history import history

admin_bp = Blueprint('admin', __name__)

ADMIN_USER = "admin"
ADMIN_PASS = "tbz2024"  # Change to your own password!

@admin_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username == ADMIN_USER and password == ADMIN_PASS:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Invalid credentials"}), 401

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    return render_template('admin.html')

@admin_bp.route('/history', methods=['GET'])
@jwt_required()
def admin_history():
    return jsonify(history)

@admin_bp.route('/devices', methods=['GET'])
@jwt_required()
def admin_devices():
    return jsonify(devices)
