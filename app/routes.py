from flask import Blueprint, render_template, request, redirect, url_for, send_file
import uuid
import os

main = Blueprint("main", __name__)
db = {}

@main.route("/")
def index():
    return render_template("form.html")

@main.route("/borrow", methods=["POST"])
def borrow():
    data = request.form
    borrow_id = str(uuid.uuid4())

    db[borrow_id] = {
        "name": data.get("name"),
        "class": data.get("class"),
        "device": data.get("device"),
        "twint_status": "unpaid"
    }

    return redirect(url_for("main.twint_qr", id=borrow_id))

@main.route("/twint/<id>")
def twint_qr(id):
    return render_template("twint.html", id=id, twint_link=f"/static/qrs/{id}.png")

@main.route("/receipt/<id>")
def receipt(id):
    return render_template("receipt.html", data=db.get(id))
