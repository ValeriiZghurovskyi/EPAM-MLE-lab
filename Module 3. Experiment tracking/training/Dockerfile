FROM python:3.9-slim

WORKDIR /app

COPY training/ ./training
COPY data/ ./data
COPY settings.json .

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "./training/train.py"]
