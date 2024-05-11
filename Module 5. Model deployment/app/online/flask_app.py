from flask import Flask, request, jsonify
import torch
import torch.nn as nn
import json
import os

app = Flask(__name__)

class IrisNet(nn.Module):
    def __init__(self):
        """Define layers of the neural network."""
        super(IrisNet, self).__init__()
        self.fc1 = nn.Linear(4, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4 = nn.Linear(32, 3)

    def forward(self, x):
        """Define the forward pass of the neural network."""
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = self.fc4(x)
        return x

def load_model(model_path):
    """Load the trained model from a file."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    model = IrisNet()
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

with open('settings.json', 'r') as f:
    settings = json.load(f)

model_name = settings['online']['model_name']

model_path = os.path.join(settings['general']['model_artifacts_dir'], model_name)

model = load_model(model_path)

@app.route('/predict', methods=['POST'])
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
    app.run(host='0.0.0.0', port=5000, debug=True)