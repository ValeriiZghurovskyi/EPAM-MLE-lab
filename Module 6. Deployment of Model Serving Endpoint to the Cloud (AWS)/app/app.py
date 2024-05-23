from flask import Flask, request, jsonify
import os
import boto3
import torch

app = Flask(__name__)

def load_model(model_name):
    """Load the trained model from a file."""
    s3 = boto3.client('s3')
    with open('model.pth', 'wb') as f:
        s3.download_fileobj('testepambucket', 'model_artifacts/{}'.format(model_name), f)
    model = torch.jit.load('model.pth')
    model.eval()
    return model

model = load_model('iris_model.pkl')

@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy."""
    return '', 200

@app.route('/invocations', methods=['POST'])
def make_predictions():
    data = request.get_json(force=True)

    if 'features' not in data:
        return jsonify({'error': 'No features in the request'}), 400

    features = data['features']

    if not isinstance(features, list) or len(features) != 4 or not all(isinstance(i, (int, float)) for i in features):
        return jsonify({'error': 'Features are not in the right format'}), 400

    features = torch.Tensor(features)

    try:
        outputs = model(features.unsqueeze(0))
        _, predicted = torch.max(outputs.data, 1)
    except Exception as err:
        return jsonify({'error': str(err)}), 500

    return jsonify(predicted.item()) 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)