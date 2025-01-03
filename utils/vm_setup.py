from api.vm_mng import create_vm, is_vm_ready
from api.net_mng import add_to_local_net

from utils.ansible_mng import update_inventory
from api.ssh_key_mng import upload_ssh_key_to_vm


def setup_vm(token, vm_name, vm_tariff, vm_disk_size, vm_image, is_backup_enabled, env_type):
    try:
        print(f"\n--- Starting setup for VM: {vm_name} ---")

        vm_data = create_vm(token, vm_name, vm_tariff, vm_disk_size, vm_image, is_backup_enabled)

        vm_id = vm_data['id']
        vm_ip = vm_data['main_ip']
        
        print(f"[INFO] VM Created Successfully - ID: {vm_id}, IP: {vm_ip}, UID: {vm_data['uid']}\n")

        print("[INFO] Checking VM readiness...\n", end=" ", flush=True)
        is_ready = is_vm_ready(token, vm_id)
        if is_ready:
            result = add_to_local_net(token, vm_name)
            print(f"[INFO] VM {vm_name} added to local network")

        else:
            print("[ERROR] VM is not ready within the specified timeout\n")
            return None

        print(f"--- Setup completed for VM: {vm_name} ---\n")
        return vm_data

    except Exception as e:
        print(f"[ERROR] Error occurred during setup of VM {vm_name}: {str(e)}\n")
        return None
