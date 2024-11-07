# Из этого скрипта родился проект

import requests
import json

API_KEY_NETANGELS = ""
api_url_token = "https://panel.netangels.ru/api/gateway/token/"
api_url_vms = "https://api-ms.netangels.ru/api/v1/cloud/vms/"

def get_token(API_KEY_NETANGELS):
    url = api_url_token
    response = requests.post(url, data={"API_KEY_NETANGELS": API_KEY_NETANGELS})

    if response.status_code == 200:
        return response.json()['token']
    else:
        raise Exception("Failed to get the token: " + response.text)

def create_vm(api_token, tariff, disk_size, image, is_backup_enabled):
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'tariff': tariff,
        'disk_size': disk_size,
        'image': image,
        'is_backup_enabled': is_backup_enabled
    }

    json_data = json.dumps(data)
    response = requests.post(api_url_vms, headers=headers, data=json_data)

    if response.status_code == 200 or response.status_code == 201:
        print("VM Created Successfully")
    else:
        raise Exception("Failed to create VM: " + response.text)
    
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

if __name__ == '__main__':
    api_token = get_token(API_KEY_NETANGELS)
    create_vm(api_token, 'start_1', 10, 'img_debian-bookworm', False)