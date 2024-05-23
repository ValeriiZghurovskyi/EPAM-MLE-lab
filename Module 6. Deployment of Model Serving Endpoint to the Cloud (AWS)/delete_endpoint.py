import boto3
import json

with open('settings.json', 'r') as f:
    settings = json.load(f)

sagemaker = boto3.client('sagemaker')

response = sagemaker.delete_endpoint(
    EndpointName=settings['EndpointName'],  
)