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
    url1 = 'https://drive.google.com/uc?id=1I4Na7bGuuNgdqYZPM_LmYZwTdf5n7nH4'
    

    settings = load_settings()

    download_file(url1, os.path.join(settings["general"]["data_dir"], settings["train"]["table_name"]))  

if __name__ == "__main__":
    main()