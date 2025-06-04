from flask import Blueprint, jsonify, request, abort, render_template

devices_bp = Blueprint('devices', __name__)

devices = [
    {
        "id": 1,
        "name": "MacBook Pro (16-inch, 2023)",
        "image": "macbook.jpg",
        "cpu": "Apple M2 Pro, 16-core CPU, 19-core GPU",
        "ram": "32GB",
        "storage": "1TB SSD",
        "display": "16-inch Retina",
        "available": True
    },
    {
        "id": 2,
        "name": "ThinkPad X1 Carbon Gen 12",
        "image": "thinkpadx1.jpg",
        "cpu": "Intel Core i7-1360P",
        "ram": "16GB",
        "storage": "1TB SSD",
        "display": "14-inch FHD+",
        "available": True
    },
    {
        "id": 3,
        "name": "HP OmniBook Ultra Flip 14",
        "image": "omnibook.jpg",
        "cpu": "Intel Core i5-1235U",
        "ram": "8GB",
        "storage": "512GB SSD",
        "display": "14-inch Touchscreen",
        "available": True
    },
    {
        "id": 4,
        "name": "HP Spectre x360",
        "image": "spectre.jpg",
        "cpu": "Intel Core i7-1255U",
        "ram": "16GB",
        "storage": "1TB SSD",
        "display": "13.5-inch OLED",
        "available": True
    },
    {
        "id": 5,
        "name": "HP Pavilion Aero 13",
        "image": "pavilion.jpg",
        "cpu": "AMD Ryzen 7 5800U",
        "ram": "16GB",
        "storage": "512GB SSD",
        "display": "13.3-inch WUXGA",
        "available": True
    },
    {
        "id": 6,
        "name": "Apple iPad Pro 13 (2024)",
        "image": "ipad.jpg",
        "cpu": "Apple M2 Chip",
        "ram": "16GB",
        "storage": "256GB Storage",
        "display": "12.9-inch Liquid Retina XDR",
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

@devices_bp.route('/<int:device_id>/return', methods=['POST'])
def return_device(device_id):
    device = next((d for d in devices if d['id'] == device_id), None)
    if not device:
        abort(404)
    if device['available']:
        return jsonify({"error": "Device is not borrowed"}), 400
    device['available'] = True
    return jsonify({"message": f"Device {device['name']} returned successfully."})