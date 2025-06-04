from flask import Blueprint, jsonify, request, abort
from datetime import datetime

history_bp = Blueprint('history', __name__)

# Einfache In-Memory-Historie (später DB)
history = []

@history_bp.route('/', methods=['GET'])
def get_history():
    return jsonify(history)

@history_bp.route('/return/<int:device_id>', methods=['POST'])
def return_device(device_id):
    # Suche das Leih-Event in history
    event = next((h for h in history if h['device_id'] == device_id and not h.get('returned')), None)
    if not event:
        return jsonify({"error": "Device not currently borrowed"}), 400

    event['returned'] = True
    event['return_date'] = datetime.now().isoformat()

    # Optional: Setze Gerät wieder auf verfügbar (muss in devices.py gemacht werden)
    # TODO: Gerätestatus aktualisieren

    return jsonify({"message": f"Device ID {device_id} returned successfully."})

@history_bp.route('/borrow', methods=['POST'])
def borrow_device():
    data = request.json
    device_id = data.get('device_id')
    user_name = data.get('user_name')

    if not device_id or not user_name:
        return jsonify({"error": "device_id and user_name required"}), 400

    # Prüfe, ob Gerät schon ausgeliehen ist
    ongoing = next((h for h in history if h['device_id'] == device_id and not h.get('returned')), None)
    if ongoing:
        return jsonify({"error": "Device already borrowed"}), 400

    new_event = {
        "device_id": device_id,
        "user_name": user_name,
        "borrow_date": datetime.now().isoformat(),
        "returned": False
    }
    history.append(new_event)

    return jsonify(new_event), 201
