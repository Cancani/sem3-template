@pdf_bp.route("/generate_receipt", methods=["POST"])
def generate_receipt():
    try:
        data = request.json
        borrower = data.get("borrower_name")
        device = data.get("device_name")
        staff = data.get("issued_by", "—")
        borrower_email = data.get("borrower_email", "")
        device_specs = data.get("device_specs", "")
        
        loan_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        return_date = datetime.now().strftime("%d.%m.%Y") + " – 17:00 Uhr"

        # Validierung der erforderlichen Daten
        if not borrower or not device:
            return jsonify({"error": "borrower_name und device_name sind erforderlich"}), 400

        html = render_template(
            "receipt.html",
            borrower=borrower,
            device=device,
            loan_date=loan_date,
            return_date=return_date,
            staff=staff,
            borrower_email=borrower_email,
            device_specs=device_specs
        )

        # PDF in Memory erstellen
        pdf_bytes = HTML(string=html).write_pdf()
        
        # PDF als direkter Download zurückgeben
        pdf_buffer = io.BytesIO(pdf_bytes)
        pdf_buffer.seek(0)
        
        # Dateiname mit Timestamp für Eindeutigkeit
        safe_borrower = "".join(c for c in borrower if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"TBZ_Quittung_{safe_borrower.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        
        response = make_response(send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        ))
        
        # CORS-Header für PowerApps
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        
        return response
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500