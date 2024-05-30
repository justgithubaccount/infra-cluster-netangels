import requests
import json
import time

from config import SSH_KEY_VALUE, SSH_KEY_ID

def create_vm(api_token, name, tariff, disk_size, image, is_backup_enabled):
    api_url_wms = "https://api-ms.netangels.ru/api/v1/cloud/vms/"

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    data = {
        'name': name,
        'tariff': tariff,
        'disk_size': disk_size,
        'image': image,
        'is_backup_enabled': is_backup_enabled,
        'key_value': SSH_KEY_VALUE,
        'key_id': SSH_KEY_ID
    }

    json_data = json.dumps(data)
    response = requests.post(api_url_wms, headers=headers, data=json_data)
    
    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()

def change_tariff(api_token, vm_name, tariff):
    vm_id = get_vm_id_by_name(api_token, vm_name)
    
    api_url_chg_tariff = f"https://api-ms.netangels.ru/api/v1/cloud/vms/{vm_id}/change-tariff/"

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'tariff': tariff
    }

    json_data = json.dumps(data)
    response = requests.post(api_url_chg_tariff, headers=headers, data=json_data)

    is_vm_ready(api_token, vm_id)

    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()

def is_vm_ready(api_token, vm_id, timeout=600, interval=10):
    """Ожидает, пока ВМ не станет активной или не истечёт таймаут"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            status = get_vm_status(api_token, vm_id)
            if status == "Active":
                print("VM is active and ready for use")
                return True
            elif status in ["Error", "StoppedByAdmin", "StoppedByService"]:
                raise Exception(f"VM cannot be activated, Status: {status}")
            print(f"Current VM status: {status}")
            time.sleep(interval)
        except Exception as e:
            print(f"Error when checking VM status: {e}")
            time.sleep(interval)
    raise TimeoutError("VM activation timeout expired")

def get_vm_status(api_token, vm_id):
    api_url_vm_id = f"https://api-ms.netangels.ru/api/v1/cloud/vms/{vm_id}/"

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(api_url_vm_id, headers=headers)
    
    if response.status_code == 200:
        return response.json()['state']
    else:
        raise Exception(f"Error API request: {response.status_code}, Response: {response.text}")

def get_vm_id_by_name(api_token, vm_name):
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
                return vm['id']
        return None # Если такой ВМ нету, возвращаем None
    else:
        raise Exception(f"Error API request: {response.status_code}, Response: {response.text}")
    
def reinstall_os(api_token, vm_name, image):
    vm_id = get_vm_id_by_name(api_token, vm_name)

    if vm_id is None:
        raise Exception("VM with the specified name does not exist.")

    # Проверка текущего статуса ВМ перед переустановкой
    status = get_vm_status(api_token, vm_id)
    if status != "Active":
        raise Exception(f"Cannot reinstall OS while VM is in '{status}' state.")

    api_url_reinstall = f"https://api-ms.netangels.ru/api/v1/cloud/vms/{vm_id}/reinstall-image/"

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'image': image
    }

    json_data = json.dumps(data)
    response = requests.post(api_url_reinstall, headers=headers, data=json_data)
    
    is_vm_ready(api_token, vm_id)

    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()
