from flask import Blueprint, render_template, request, redirect, url_for
import uuid

main = Blueprint("main", __name__)

# Dummy devices
devices = [
    {"name": "iPad Pro", "description": "12.9 inch, 256GB"},
    {"name": "Surface Laptop", "description": "13.5 inch, i7"},
    {"name": "MacBook Air", "description": "M2, 512GB"},
]

# Temporary in-memory store
borrowed = {}

@main.route("/")
def home():
    return render_template("home.html", devices=devices)

@main.route("/form/<device>")
def form(device):
    return render_template("form.html", device=device)

@main.route("/borrow", methods=["POST"])
def borrow():
    data = request.form
    borrow_id = str(uuid.uuid4())
    borrowed[borrow_id] = {
        "name": data.get("name"),
        "class": data.get("class"),
        "device": data.get("device"),
        "return_date": data.get("return_date"),
    }
    # Placeholder QR code (use static image or generate later)
    return redirect(url_for("main.twint", id=borrow_id))

@main.route("/twint/<id>")
def twint(id):
    qr_url = "/static/qr_placeholder.png"  # TODO: Replace with real QR
    return render_template("twint.html", borrow_id=id, qr_url=qr_url)

@main.route("/confirm/<id>")
def confirm(id):
    return render_template("confirm.html")
