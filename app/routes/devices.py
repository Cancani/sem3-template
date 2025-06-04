from flask import Blueprint, jsonify, request, abort

devices_bp = Blueprint('devices', __name__)

# Beispiel-Daten (Später Datenbank oder CSV)
devices = [
    {"id": 1, "name": "Laptop 1", "description": "Lenovo ThinkPad", "available": True},
    {"id": 2, "name": "Adapter USB-C", "description": "USB-C auf HDMI Adapter", "available": True},
]

@devices_bp.route('/', methods=['GET'])
def list_devices():
    return jsonify(devices)

@devices_bp.route('/<int:device_id>', methods=['GET'])
def get_device(device_id):
    device = next((d for d in devices if d['id'] == device_id), None)
    if not device:
        abort(404)
    return jsonify(device)

@devices_bp.route('/<int:device_id>/borrow', methods=['POST'])
def borrow_device(device_id):
    device = next((d for d in devices if d['id'] == device_id), None)
    if not device:
        abort(404)
    if not device['available']:
        return jsonify({"error": "Device is already borrowed"}), 400

    # Beispiel: Markiere als ausgeliehen
    device['available'] = False
    # Hier könntest du Validierung, Logging, Quittungserstellung usw. einbauen

    return jsonify({"message": f"Device {device['name']} borrowed successfully."})
