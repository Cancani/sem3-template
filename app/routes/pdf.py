from flask import Blueprint, request, send_file, render_template
from datetime import datetime
from weasyprint import HTML
import re
import sys

pdf_bp = Blueprint("pdf", __name__)

@pdf_bp.route("/generate_receipt", methods=["POST"])
def generate_receipt():
    # Log: Endpoint wurde aufgerufen
    print("Route /generate_receipt wurde aufgerufen", file=sys.stderr)
    data = request.json
    print("Empfangene Daten:", data, file=sys.stderr)

    # Pflichtfelder
    borrower = data.get("borrower")
    device = data.get("device")
    # Optional: staff, Default-Strich wenn leer
    staff = data.get("staff", "—")

    # Datum berechnen
    loan_date = datetime.now().strftime("%d.%m.%Y %H:%M")
    return_date = datetime.now().strftime("%d.%m.%Y") + " – 17:00 Uhr"

    # HTML-Template rendern
    try:
        html = render_template(
            "receipt.html",
            borrower=borrower,
            device=device,
            loan_date=loan_date,
            return_date=return_date,
            staff=staff
        )
        print("HTML wurde erfolgreich gerendert", file=sys.stderr)
    except Exception as e:
        print("Fehler beim Rendern des Templates:", e, file=sys.stderr)
        raise

    # PDF erstellen
    pdf_path = "/tmp/receipt.pdf"
    try:
        HTML(string=html).write_pdf(pdf_path)
        print("PDF wurde erfolgreich erstellt", file=sys.stderr)
    except Exception as e:
        print("Fehler beim Erstellen des PDFs:", e, file=sys.stderr)
        raise

    # Sicheren Dateinamen aus borrower erzeugen (keine Sonderzeichen)
    if borrower:
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '', borrower.replace(' ', '_'))
    else:
        safe_name = 'Unbekannt'
    filename = f"{safe_name}_1.pdf"

    # PDF als Download zurückgeben
    return send_file(pdf_path, as_attachment=True, download_name=filename)
