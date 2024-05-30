import requests

from api.vm_mng import get_vm_id_by_name

def add_to_local_net(api_token, vm_name):
    vm_id = get_vm_id_by_name(api_token, vm_name)

    if vm_id is None:
        raise ValueError("VM not found")

    api_lan_cloud = f"https://api-ms.netangels.ru/api/v1/cloud/vms/{vm_id}/lan/"

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(api_lan_cloud, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")