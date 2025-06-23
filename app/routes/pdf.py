from flask import Blueprint, request, jsonify, render_template, send_file, make_response
from datetime import datetime
from weasyprint import HTML
import base64
import os
import io

pdf_bp = Blueprint("pdf", __name__)

@pdf_bp.route("/generate_receipt", methods=["POST"])
def generate_receipt():
    try:
        data = request.json
        borrower = data.get("borrower_name")
        device = data.get("device_name")
        staff = data.get("issued_by", "—")
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