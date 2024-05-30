import requests

def get_token(api_key):
    api_url_token="https://panel.netangels.ru/api/gateway/token/"

    response = requests.post(api_url_token, data={"api_key": api_key})
    
    if response.status_code == 200:
        return response.json()['token']
    else:
        raise Exception("Failed to get token: " + response.text)