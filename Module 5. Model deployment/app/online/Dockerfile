FROM python:3.9-slim

WORKDIR /app

COPY app/online/ ./online
COPY app/model_artifacts/ ./model_artifacts
COPY app/settings.json .

RUN pip install --no-cache-dir -r online/requirements.txt

EXPOSE 5000

CMD ["python", "online/flask_app.py"]
