import requests
import json
import os

def load_settings():
    with open("settings.json", "r") as file:
        settings = json.load(file)
    return settings

def download_file(url, destination):
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(destination, 'wb') as f:
        f.write(response.content)

def main():
    url1 = 'https://drive.google.com/uc?id=1m5banV29WJy_8qdwibb0J8M7UVO78y5w'
    url2 = 'https://drive.google.com/uc?id=1phM9u8Uj7UBpC3t51_nqfqwtp4Fml06H'

    settings = load_settings()

    download_file(url1, os.path.join(settings["general"]["data_dir"], settings["inference"]["inp_table_name"]))  
    download_file(url2, os.path.join(settings["general"]["models_dir"], settings["inference"]["model_name"]))  

if __name__ == "__main__":
    main()
