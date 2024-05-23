import boto3
import json

with open('settings.json', 'r') as f:
    settings = json.load(f)

runtime = boto3.client('sagemaker-runtime')

response = runtime.invoke_endpoint(
    EndpointName=settings['EndpointName'],  
    ContentType='application/json', 
    Body=json.dumps(settings['InputData']),  
)

print(response['Body'].read())