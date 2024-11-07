import requests
import json
import time
from config import SSH_KEY_PUBLIC, SSH_KEY_PUBLIC_ID

def create_vm(token, vm_name, vm_tariff, vm_disk_size, vm_image, is_backup_enabled):
    api_url_wms = "https://api-ms.netangels.ru/api/v1/cloud/vms/"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    json_data = {
        "name": vm_name,
        "tariff": vm_tariff,
        "disk_size": vm_disk_size,
        "image": vm_image,
        "is_backup_enabled": is_backup_enabled
    }
    
    print(f"[INFO] Creating VM with the following parameters:\n{json.dumps(json_data, indent=2)}")
    
    response = requests.post(api_url_wms, headers=headers, json=json_data)
    
    if response.status_code == 201:
        vm_data = response.json()
        print(f"[SUCCESS] VM created successfully - ID: {vm_data['id']}, Name: {vm_data['name']}")
        return vm_data
    else:
        print(f"[ERROR] Failed to create VM. Response: {response.text}")
        response.raise_for_status()

def change_tariff(api_token, vm_name, tariff):
    print(f"[INFO] Attempting to change tariff for VM '{vm_name}' to '{tariff}'")
    vm_id = get_vm_id_by_name(api_token, vm_name)
    
    if not vm_id:
        print(f"[ERROR] VM with name '{vm_name}' not found.")
        return

    api_url_chg_tariff = f"https://api-ms.netangels.ru/api/v1/cloud/vms/{vm_id}/change-tariff/"
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    data = {'tariff': tariff}
    print(f"[INFO] Changing tariff with data: {json.dumps(data, indent=2)}")
    response = requests.post(api_url_chg_tariff, headers=headers, json=data)

    if response.status_code == 201:
        print(f"[SUCCESS] Tariff changed successfully for VM ID: {vm_id}")
        return response.json()
    else:
        print(f"[ERROR] Failed to change tariff. Response: {response.text}")
        response.raise_for_status()

def is_vm_ready(api_token, vm_id, timeout=600, interval=10):
    """Ожидает, пока ВМ не станет активной или не истечёт таймаут"""
    start_time = time.time()
    last_status = None  # Хранение последнего статуса для предотвращения дублирования вывода
    
    print(f"[INFO] Checking readiness of VM (ID: {vm_id}) with a timeout of {timeout} seconds.")

    while time.time() - start_time < timeout:
        try:
            status = get_vm_status(api_token, vm_id)
            # Выводим статус только если он изменился
            if status != last_status:
                print(f"[STATUS] Current VM status: {status}")
                last_status = status
            
            if status == "Active":
                print("[SUCCESS] VM is active and ready for use.")
                return True
            elif status in ["Error", "StoppedByAdmin", "StoppedByService"]:
                raise Exception(f"[ERROR] VM cannot be activated. Final status: {status}")

            time.sleep(interval)

        except Exception as e:
            print(f"[ERROR] Exception during VM status check: {e}")
            time.sleep(interval)
    
    raise TimeoutError(f"[TIMEOUT] VM (ID: {vm_id}) was not ready within {timeout} seconds.")

def get_vm_status(api_token, vm_id):
    api_url_vm_id = f"https://api-ms.netangels.ru/api/v1/cloud/vms/{vm_id}/"
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    print(f"[INFO] Fetching status for VM ID: {vm_id}")
    response = requests.get(api_url_vm_id, headers=headers)
    
    if response.status_code == 200:
        status = response.json()['state']
        print(f"[INFO] Status of VM ID {vm_id}: {status}")
        return status
    else:
        error_message = f"[ERROR] Failed to fetch VM status. Response: {response.text}"
        print(error_message)
        raise Exception(error_message)

def get_vm_id_by_name(api_token, vm_name):
    api_url_vms_list = "https://api-ms.netangels.ru/api/v1/cloud/vms/"
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    print(f"[INFO] Searching for VM by name: {vm_name}")
    response = requests.get(api_url_vms_list, headers=headers)

    if response.status_code == 200:
        vms = response.json()

        # Перебор всех ВМ в json
        for vm in vms['entities']:
            if vm['name'] == vm_name:
                print(f"[INFO] Found VM '{vm_name}' with ID: {vm['id']}")
                return vm['id']
        print(f"[WARNING] VM with name '{vm_name}' not found.")
        return None  # Если такой ВМ нет, возвращаем None
    else:
        error_message = f"[ERROR] Failed to fetch VM list. Response: {response.text}"
        print(error_message)
        raise Exception(error_message)

def reinstall_os(api_token, vm_name, image):
    print(f"[INFO] Starting OS reinstallation for VM '{vm_name}' with image '{image}'")
    vm_id = get_vm_id_by_name(api_token, vm_name)

    if not vm_id:
        print(f"[ERROR] VM with name '{vm_name}' not found.")
        return

    # Проверка текущего статуса ВМ перед переустановкой
    status = get_vm_status(api_token, vm_id)
    if status != "Active":
        error_message = f"[ERROR] Cannot reinstall OS while VM is in '{status}' state."
        print(error_message)
        raise Exception(error_message)

    api_url_reinstall = f"https://api-ms.netangels.ru/api/v1/cloud/vms/{vm_id}/reinstall-image/"
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    
    data = {'image': image}
    print(f"[INFO] Sending reinstallation request with data: {json.dumps(data, indent=2)}")
    response = requests.post(api_url_reinstall, headers=headers, json=data)

    if response.status_code == 201:
        print(f"[SUCCESS] OS reinstallation initiated for VM ID: {vm_id}")
        return response.json()
    else:
        error_message = f"[ERROR] Failed to reinstall OS. Response: {response.text}"
        print(error_message)
        response.raise_for_status()
