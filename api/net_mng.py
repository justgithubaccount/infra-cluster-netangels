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
    
def get_vm_lan_ip(api_token, vm_name):
    api_url_vms_list = "https://api-ms.netangels.ru/api/v1/cloud/vms/"

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(api_url_vms_list, headers=headers)

    if response.status_code == 200:
        vms = response.json()

        # Перебор всех ВМ в json
        for vm in vms['entities']:
            if vm['name'] == vm_name:
                return vm['lan_ip']
        return None # Если такой ВМ нету, возвращаем None
    else:
        raise Exception(f"Error API request: {response.status_code}, Response: {response.text}")