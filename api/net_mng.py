import requests

from api.vm_mng import get_vm_id_by_name

def add_to_local_net(api_token, vm_name):
    print(f"[INFO] Initiating request to add VM '{vm_name}' to local network.")
    vm_id = get_vm_id_by_name(api_token, vm_name)

    if vm_id is None:
        error_message = f"[ERROR] VM '{vm_name}' not found. Cannot proceed with LAN addition."
        print(error_message)
        raise ValueError(error_message)

    api_lan_cloud = f"https://api-ms.netangels.ru/api/v1/cloud/vms/{vm_id}/lan/"
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    print(f"[DEBUG] Sending request to add VM (ID: {vm_id}) to LAN with endpoint: {api_lan_cloud}")
    response = requests.post(api_lan_cloud, headers=headers)
    
    if response.status_code == 200:
        print(f"[SUCCESS] VM '{vm_name}' (ID: {vm_id}) successfully added to local network.")
        return response.json()
    else:
        error_message = f"[ERROR] Failed to add VM '{vm_name}' to local network. Status: {response.status_code}, Response: {response.text}"
        print(error_message)
        raise Exception(error_message)

def get_vm_lan_ip(api_token, vm_name):
    print(f"[INFO] Fetching LAN IP for VM '{vm_name}'.")
    api_url_vms_list = "https://api-ms.netangels.ru/api/v1/cloud/vms/"

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    print("[DEBUG] Sending request to retrieve VMs list for LAN IP search.")
    response = requests.get(api_url_vms_list, headers=headers)

    if response.status_code == 200:
        vms = response.json()
        for vm in vms['entities']:
            if vm['name'] == vm_name:
                lan_ip = vm.get('lan_ip')
                print(f"[SUCCESS] LAN IP for VM '{vm_name}' found: {lan_ip}")
                return lan_ip
        print(f"[WARNING] VM '{vm_name}' not found in VMs list.")
        return None
    else:
        error_message = f"[ERROR] Failed to retrieve VMs list. Status: {response.status_code}, Response: {response.text}"
        print(error_message)
        raise Exception(error_message)
