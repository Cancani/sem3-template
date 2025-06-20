from flask import Flask
from app.routes.pdf import pdf_bp

app = Flask(__name__)
app.register_blueprint(pdf_bp)

@app.route("/")
def index():
    return "PDF Microservice is running"
