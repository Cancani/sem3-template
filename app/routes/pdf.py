from flask import Blueprint, request, send_file, render_template
from datetime import datetime
import os
import pdfkit

pdf_bp = Blueprint("pdf", __name__)

@pdf_bp.route("/generate_receipt", methods=["POST"])
def generate_receipt():
    data = request.json

    borrower = data.get("borrower")
    device = data.get("device")
    loan_date = datetime.now().strftime("%d.%m.%Y %H:%M")
    return_date = datetime.now().strftime("%d.%m.%Y") + " – 17:00 Uhr"

    html = render_template("receipt.html",
        borrower=borrower,
        device=device,
        loan_date=loan_date,
        return_date=return_date,
        amount="CHF 20.–"
    )

    pdf_path = "/tmp/receipt.pdf"
    pdfkit.from_string(html, pdf_path)

    return send_file(pdf_path, as_attachment=True, download_name="quittung.pdf")
