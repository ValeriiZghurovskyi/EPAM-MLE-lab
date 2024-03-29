import os
import json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import logging

class IrisNet(nn.Module):
    def __init__(self):
        super(IrisNet, self).__init__()
        self.fc1 = nn.Linear(4, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4 = nn.Linear(32, 3)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = self.fc4(x)
        return x

def load_model(model_path):
    model = IrisNet()
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=1, keepdims=True)

def run_inference(model, data):
    with torch.no_grad():
        predictions = model(data)
    return predictions

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # with open('../settings.json') as f:
    #     settings = json.load(f)
    with open('settings.json') as f:
        settings = json.load(f)

    # model_path = "../" + settings['general']['models_dir'] + "/" + settings['inference']['model_name']
    # inference_data_path = "../" + settings['general']['data_dir'] + "/" + settings['inference']['inp_table_name']
    model_path = settings['general']['models_dir'] + "/" + settings['inference']['model_name']
    inference_data_path = settings['general']['data_dir'] + "/" + settings['inference']['inp_table_name']

    model = load_model(model_path)
    logging.info(f"Loaded model from {model_path}")

    inference_data = pd.read_csv(inference_data_path)
    logging.info(f"Loaded inference data from {inference_data_path}")

    X_inference = torch.tensor(inference_data.iloc[:, :4].values, dtype=torch.float32)

    logits = run_inference(model, X_inference).numpy()
    probabilities = softmax(logits)
    predicted_classes = np.argmax(probabilities, axis=1)

    results = pd.DataFrame({
        'Predicted Class': predicted_classes,
        'Probability Class 0': probabilities[:, 0],
        'Probability Class 1': probabilities[:, 1],
        'Probability Class 2': probabilities[:, 2]
    })

    # results_dir = "../" + settings['general']['results_dir']
    # if not os.path.exists(results_dir):
    #     os.makedirs(results_dir)

    results_dir = settings['general']['results_dir']
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    results_path = results_dir + "/inference_results.csv"
    results.to_csv(results_path, index=False)

    logging.info(f"Saved inference results to {results_path}")