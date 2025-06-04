from weasyprint import HTML
from datetime import datetime
import os

def generate_receipt(data: dict, output_file: str):
    """
    Generiert eine PDF-Quittung mit den übergebenen Daten.

    data: dict mit z.B. device_name, user_name, date, amount
    output_file: Pfad, wo PDF gespeichert wird
    """

    html_content = f"""
    <html>
    <head>
      <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #007bff; }}
        p {{ font-size: 14px; }}
      </style>
    </head>
    <body>
      <h1>Quittung Geräteausleihe</h1>
      <p><strong>Gerät:</strong> {data.get('device_name')}</p>
      <p><strong>Benutzer:</strong> {data.get('user_name')}</p>
      <p><strong>Datum:</strong> {data.get('date', datetime.now().strftime('%Y-%m-%d %H:%M'))}</p>
      <p><strong>Betrag:</strong> {data.get('amount', 'TWINT (statisch)')}</p>
      <hr>
      <p>Vielen Dank für die Nutzung unseres Ausleihservices.</p>
    </body>
    </html>
    """

    HTML(string=html_content).write_pdf(output_file)

    return output_file
