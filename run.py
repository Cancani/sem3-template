from flask import Flask
from app.routes.pdf import pdf_bp

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
app.register_blueprint(pdf_bp)

@app.route('/')
def index():
    return 'PDF Microservice is running'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

#Push