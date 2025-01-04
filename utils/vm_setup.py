from api.vm_mng import create_vm, is_vm_ready
from api.net_mng import add_to_local_net

from utils.ansible_mng import update_inventory
from api.ssh_key_mng import upload_ssh_key_to_vm


def setup_vm(token, vm_name, vm_tariff, vm_disk_size, vm_image, is_backup_enabled, env_type):
    try:
        print(f"\n--- Starting setup for VM: {vm_name} ---")

        # VM Create
        vm_data = create_vm(token, vm_name, vm_tariff, vm_disk_size, vm_image, is_backup_enabled)

        vm_id = vm_data['id']
        vm_ip = vm_data['main_ip']
        vm_uid = vm_data['uid']
        
        print(f"[INFO] VM Created Successfully - ID: {vm_id}, IP: {vm_ip}, UID: {vm_uid}\n")

        # Add to LAN
        if is_vm_ready(token, vm_id): 
            add_to_local_net(token, vm_name)
            print(f"[INFO] VM {vm_name} added to local network")
        else:
            print("[ERROR] VM is not ready within the specified timeout\n")
            return None
        
        # SSH Key
        upload_response = upload_ssh_key_to_vm(token, vm_name)
        if upload_response:  # Проверяем, что функция вернула не None
            print(f"[INFO] SSH Key successfully uploaded to VM: {vm_name}")
            print(f"[DEBUG] Uploaded SSH Key details: {upload_response}")  # Логируем детали ключа
        else:
            print(f"[WARNING] Failed to upload SSH key to VM: {vm_name}. Check logs for details.")

        print(f"--- Setup completed for VM: {vm_name} ---\n")
        return vm_data

    except Exception as e:
        print(f"[ERROR] Error occurred during setup of VM {vm_name}: {str(e)}\n")
        return None
