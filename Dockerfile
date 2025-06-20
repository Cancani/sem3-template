# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# System-Abhängigkeiten für PDF (wkhtmltopdf)
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]
