# https://api.netangels.ru/modules/gateway_api.api.cloud.sshkeys/#ssh-_2

import requests
import json

from config import SSH_KEY_ID

from api.vm_mng import get_vm_id_by_name

def upload_ssh_key_to_vm(api_token, vm_name):
    vm_id = get_vm_id_by_name(api_token, vm_name)

    api_url_ssh = f"https://api-ms.netangels.ru//api/v1/cloud/vms/{vm_id}/ssh/upload/"

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    data = {
        "key_id": SSH_KEY_ID 
    }

    json_data = json.dumps(data)
    response = requests.post(api_url_ssh, headers=headers, data=json_data)

    return response