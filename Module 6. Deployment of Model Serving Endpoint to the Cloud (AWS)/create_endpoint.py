import boto3
import json

with open('settings.json', 'r') as f:
    settings = json.load(f)

sagemaker = boto3.client('sagemaker')

response = sagemaker.create_endpoint_config(
    EndpointConfigName=settings['EndpointConfigName'],
    ProductionVariants=[
        {
            'VariantName': 'default',
            'ModelName': settings['ModelName'],
            'InitialInstanceCount': 1,
            'InstanceType': settings['InstanceType'],
        },
    ]
)

response = sagemaker.create_endpoint(
    EndpointName=settings['EndpointName'],
    EndpointConfigName=settings['EndpointConfigName'],
)