FROM python:3.9-slim

LABEL authors="abylayaitbanov"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENTRYPOINT ["python", "app.py"]