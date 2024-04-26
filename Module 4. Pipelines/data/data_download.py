import requests
import os

def download_file(url, destination):
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(destination, 'wb') as f:
        f.write(response.content)


def main():
    url1 = 'https://drive.google.com/uc?id=1tUiXu4wO3rs8IEQXGqOFWiBdNzuPKJeJ'
    download_file(url1, './data/shops.csv')

    url2 = 'https://drive.google.com/uc?id=1V7zWnBHXE4H2KRYlp1aRZWbPmO2DnUDL'
    download_file(url2, './data/sales_train.csv')

    url3 = 'https://drive.google.com/uc?id=1Y8wQDshnAVP4mAp2qyBtPPIdbpQAIJHF'
    download_file(url3, './data/items.csv')

    url4 = 'https://drive.google.com/uc?id=13U_pOK8vqiEY0ywKE1vk6wf3NK8fZbjB'
    download_file(url4, './data/item_categories.csv')

if __name__ == "__main__":
    main()