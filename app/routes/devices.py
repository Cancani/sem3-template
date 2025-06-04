from flask import Blueprint, jsonify, request, abort, render_template

devices_bp = Blueprint('devices', __name__)

devices = [
    {
        "id": 1,
        "name": "MacBook Pro (16-inch, 2023)",
        "description": "Apple M2 Pro, 16-core CPU, 19-core GPU, 32GB RAM, 1TB SSD",
        "available": True
    },
    {
        "id": 2,
        "name": "ThinkPad X1 Carbon Gen 12",
        "description": "Intel Core i7-1360P, 16GB RAM, 1TB SSD, 14-inch FHD+ Display",
        "available": True
    },
    {
        "id": 3,
        "name": "HP OmniBook Ultra Flip 14",
        "description": "Intel Core i5-1235U, 8GB RAM, 512GB SSD, 14-inch Touchscreen",
        "available": True
    },
    {
        "id": 4,
        "name": "HP Spectre x360",
        "description": "Intel Core i7-1255U, 16GB RAM, 1TB SSD, 13.5-inch OLED Display",
        "available": True
    },
    {
        "id": 5,
        "name": "HP Pavilion Aero 13",
        "description": "AMD Ryzen 7 5800U, 16GB RAM, 512GB SSD, 13.3-inch WUXGA Display",
        "available": True
    },
    {
        "id": 6,
        "name": "Apple iPad Pro 13 (2024)",
        "description": "Apple M2 Chip, 16GB RAM, 256GB Storage, 12.9-inch Liquid Retina XDR Display",
        "available": True
    }
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

    device['available'] = False
    return jsonify({"message": f"Device {device['name']} borrowed successfully."})

@devices_bp.route('/dashboard')
def dashboard():
    return render_template('home.html')
