from flask import Flask
from app.routes.pdf import pdf_bp  # <--- Importiere den Blueprint

app = Flask(__name__)
app.register_blueprint(pdf_bp)  # <--- Registriere den Blueprint

@app.route('/')
def index():
    return 'PDF Microservice is running'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
