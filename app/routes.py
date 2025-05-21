from flask import Blueprint, render_template, request

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("form.html")

@main.route("/borrow", methods=["POST"])
def borrow():
    name = request.form.get("name")
    device = request.form.get("device")
    return f"Thanks {name}, you've borrowed: {device}"
