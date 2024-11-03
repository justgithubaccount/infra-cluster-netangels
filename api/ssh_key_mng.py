# https://api.netangels.ru/modules/gateway_api.api.cloud.sshkeys/#ssh-_2

import requests
import json

from config import SSH_KEY_ID

from api.vm_mng import get_vm_id_by_name

def upload_ssh_key_to_vm(api_token, vm_name):
    vm_id = get_vm_id_by_name(api_token, vm_name)
    if not vm_id:
        print(f"VM '{vm_name}' not found.")
        return None

    api_url_ssh = f"https://api-ms.netangels.ru/api/v1/cloud/vms/{vm_id}/ssh/upload/"
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "key_id": SSH_KEY_ID
    }

    response = requests.post(api_url_ssh, headers=headers, json=data)  # Отправляем JSON напрямую
    try:
        response.raise_for_status()  # Проверка на ошибки HTTP
        print(f"SSH key successfully uploaded to VM '{vm_name}' (ID: {vm_id}).")
        return response.json()  # Возвращает ответ, если требуется
    except requests.exceptions.HTTPError as e:
        # Обработка ошибок HTTP
        if response.status_code == 404:
            print(f"SSH key with ID '{SSH_KEY_ID}' or VM with ID '{vm_id}' not found.")
        elif response.status_code == 400:
            print("Invalid request format or missing required parameters.")
        else:
            print(f"Failed to upload SSH key: {e}")
        print("Response:", response.json())  # Вывод ответа для отладки
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None