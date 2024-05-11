import pytest
import json
import os
import pandas as pd
import sys

test_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(test_dir)

sys.path.insert(0, app_dir)
from batch.predict import load_model, IrisNet

def test_load_model():
    script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    settings_file_path = os.path.join(script_dir, "settings.json")
    with open(settings_file_path, 'r') as f:
        settings = json.load(f)
    general_settings = settings["general"]
    batch_settings = settings["batch"]
    model_path = os.path.join(script_dir, general_settings["model_artifacts_dir"], batch_settings["model_name"])    
    try:
        model = load_model(model_path)
        assert isinstance(model, IrisNet)
    except FileNotFoundError:
        pytest.fail(f"Model file not found: {model_path}")

def test_settings_file_exists():
    script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    settings_file_path = os.path.join(script_dir, "settings.json")
    assert os.path.exists(settings_file_path) == True

def test_settings_file_format():
    script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    settings_file_path = os.path.join(script_dir, "settings.json")
    try:
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
        assert isinstance(settings, dict)
    except ValueError:
        pytest.fail(f"File {settings_file_path} is not a valid JSON")
