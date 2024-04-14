FROM python:3.9-slim

WORKDIR /app

RUN pip install mlflow==2.11.3 

EXPOSE 5000

CMD mlflow server \
    --backend-store-uri file:///mlflow_server \
    --default-artifact-root file:///mlflow_server/artifacts \
    --host 0.0.0.0