from flask import Blueprint, request, jsonify, render_template, send_file, make_response
from datetime import datetime
from weasyprint import HTML
import base64
import os
import io
import uuid
import json
from urllib.parse import quote

pdf_bp = Blueprint("pdf", __name__)

# Temporärer Speicher für PDF-Daten (in Produktion: Redis/Database)
pdf_storage = {}

@pdf_bp.route("/generate_receipt_link", methods=["POST"])
def generate_receipt_link():
    try:
        data = request.json
        borrower = data.get("borrower_name")
        device = data.get("device_name")
        staff = data.get("issued_by", "IT-Support TBZ")
        
        if not borrower or not device:
            return jsonify({"error": "borrower_name und device_name sind erforderlich"}), 400

        # Unique ID generieren
        pdf_id = str(uuid.uuid4())
        
        # PDF-Daten speichern
        pdf_storage[pdf_id] = {
            "borrower": borrower,
            "device": device,
            "staff": staff,
            "created": datetime.now(),
            "expires": datetime.now().timestamp() + 3600  # 1 Stunde gültig
        }
        
        # Download-Link generieren
        download_link = f"http://54.87.172.226:5000/download_receipt/{pdf_id}"
        
        return jsonify({
            "pdf_link": download_link,
            "pdf_id": pdf_id,
            "expires_in": "1 hour"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pdf_bp.route("/download_receipt/<pdf_id>", methods=["GET"])
def download_receipt(pdf_id):
    try:
        # Prüfen ob PDF-ID existiert
        if pdf_id not in pdf_storage:
            return jsonify({"error": "PDF nicht gefunden oder abgelaufen"}), 404
        
        pdf_data = pdf_storage[pdf_id]
        
        # Prüfen ob abgelaufen
        if datetime.now().timestamp() > pdf_data["expires"]:
            del pdf_storage[pdf_id]
            return jsonify({"error": "PDF-Link ist abgelaufen"}), 410
        
        # PDF generieren
        loan_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        return_date = datetime.now().strftime("%d.%m.%Y") + " – 17:00 Uhr"
        
        html = render_template(
            "receipt.html",
            borrower=pdf_data["borrower"],
            device=pdf_data["device"],
            loan_date=loan_date,
            return_date=return_date,
            staff=pdf_data["staff"]
        )

        pdf_bytes = HTML(string=html).write_pdf()
        pdf_buffer = io.BytesIO(pdf_bytes)
        pdf_buffer.seek(0)
        
        safe_borrower = "".join(c for c in pdf_data["borrower"] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"TBZ_Quittung_{safe_borrower.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        
        # PDF nach Download löschen
        del pdf_storage[pdf_id]
        
        response = make_response(send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        ))
        
        return response
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Behalte die ursprüngliche POST-Route für Tests
@pdf_bp.route("/generate_receipt", methods=["POST"])
def generate_receipt():
    try:
        data = request.json
        borrower = data.get("borrower_name")
        device = data.get("device_name")
        staff = data.get("issued_by", "IT-Support TBZ")
        loan_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        return_date = datetime.now().strftime("%d.%m.%Y") + " – 17:00 Uhr"

        if not borrower or not device:
            return jsonify({"error": "borrower_name und device_name sind erforderlich"}), 400

        html = render_template(
            "receipt.html",
            borrower=borrower,
            device=device,
            loan_date=loan_date,
            return_date=return_date,
            staff=staff
        )

        pdf_bytes = HTML(string=html).write_pdf()
        pdf_buffer = io.BytesIO(pdf_bytes)
        pdf_buffer.seek(0)
        
        safe_borrower = "".join(c for c in borrower if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"TBZ_Quittung_{safe_borrower.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        
        response = make_response(send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        ))
        
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        
        return response
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pdf_bp.route("/generate_receipt", methods=["OPTIONS"])
def handle_options():
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response