import torch
import pandas as pd
import os
import torch
import torch.nn as nn
import json
from datetime import datetime


def load_model(model_path):
    """Load the trained model from a file."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    model = torch.jit.load(model_path)
    model.eval()
    return model

def batch_predict(input_file, output_file, model_path):
    model = load_model(model_path)

    df = pd.read_csv(input_file)

    input_tensor = torch.Tensor(df.values)

    with torch.no_grad():
        outputs = model(input_tensor)
        _, predicted = torch.max(outputs.data, 1)

    pd.DataFrame(predicted.numpy()).to_csv(output_file, header=False, index=False)

    print(f"{datetime.now()} - Prediction completed. Output file: {output_file}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    settings_file_path = os.path.join(script_dir, "settings.json")
    with open(settings_file_path, 'r') as f:
        settings = json.load(f)
    
    general_settings = settings["general"]
    batch_settings = settings["batch"]
    
    input_file = os.path.join(script_dir, general_settings["data_dir"], batch_settings["inp_table_name"])
    output_file = os.path.join(script_dir, general_settings["data_dir"], batch_settings["result_table_name"])
    model_path = os.path.join(script_dir, general_settings["model_artifacts_dir"], batch_settings["model_name"])

    batch_predict(input_file, output_file, model_path)