import requests
import json

from config import SSH_KEY_PUBLIC_ID
from api.vm_mng import get_vm_id_by_name

def upload_ssh_key_to_vm(api_token, vm_name):
    print(f"[INFO] Initiating SSH key upload to VM: {vm_name}")
    vm_id = get_vm_id_by_name(api_token, vm_name)
    if not vm_id:
        print(f"[ERROR] VM '{vm_name}' not found. Cannot proceed with SSH key upload.")
        return None

    api_url_ssh = f"https://api-ms.netangels.ru/api/v1/cloud/vms/{vm_id}/ssh/upload/"
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "key_id": SSH_KEY_PUBLIC_ID
    }

    print(f"[DEBUG] Uploading SSH key to VM '{vm_name}' (ID: {vm_id}) with key ID: {SSH_KEY_PUBLIC_ID}")
    response = requests.post(api_url_ssh, headers=headers, json=data)

    if response.status_code == 200:
        ssh_key_data = response.json()
        print(f"[SUCCESS] SSH key successfully uploaded to VM '{vm_name}' (ID: {vm_id}).")
        return ssh_key_data
    elif response.status_code == 404:
        print(f"[ERROR] SSH key with ID '{SSH_KEY_PUBLIC_ID}' or VM with ID '{vm_id}' not found.")
    elif response.status_code == 400:
        print("[ERROR] Invalid request format or missing required parameters.")
    else:
        print(f"[ERROR] Failed to upload SSH key. Unexpected HTTP error: {response.status_code}")

    try:
        print("[DEBUG] Response content:", response.json())
    except json.JSONDecodeError:
        print("[DEBUG] Response content could not be decoded.")

    return None
