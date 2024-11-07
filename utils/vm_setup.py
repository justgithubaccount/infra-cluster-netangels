from api.vm_mng import create_vm, is_vm_ready
from api.net_mng import add_to_local_net

from utils.ansible_mng import update_inventory
from api.ssh_key_mng import upload_ssh_key_to_vm


def setup_vm(token, vm_name, vm_tariff, vm_disk_size, vm_image, is_backup_enabled, env_type):
    try:
        print(f"\n--- Starting setup for VM: {vm_name} ---")
        print(f"Requested configuration: Name: {vm_name}, Tariff: {vm_tariff}, Disk Size: {vm_disk_size} GB, Image: {vm_image}, Backup Enabled: {is_backup_enabled}\n")

        # Step 1: Create VM
        vm_data = create_vm(token, vm_name, vm_tariff, vm_disk_size, vm_image, is_backup_enabled)
        vm_id = vm_data['id']
        vm_ip = vm_data['main_ip']

        print(f"[INFO] VM Created Successfully - ID: {vm_id}, IP: {vm_ip}, UID: {vm_data['uid']}\n")

        # Step 2: Check VM Readiness
        print("[INFO] Checking VM readiness...\n", end=" ", flush=True)
        if is_vm_ready(token, vm_id):
            print("Ready\n")

            # Step 3: Add VM to Local Network
            add_to_local_net(token, vm_name)
            print(f"[INFO] VM {vm_name} added to local network")

            # Step 4: Upload SSH Key
            upload_response = upload_ssh_key_to_vm(token, vm_name)
            if upload_response.status_code == 200:
                print(f"[INFO] SSH Key successfully uploaded to VM: {vm_name}")
            else:
                print(f"[WARNING] Failed to upload SSH key to VM: {vm_name}. Response: {upload_response.text}")

            # Step 5: Update Inventory
            update_inventory(token, vm_name, vm_ip, "server", env_type)
            print(f"[INFO] Inventory updated for VM: {vm_name} - IP: {vm_ip}, Environment: {env_type}\n")
        else:
            print("[ERROR] VM is not ready within the specified timeout\n")
            return None

        print(f"--- Setup completed for VM: {vm_name} ---\n")
        return vm_data
    except Exception as e:
        print(f"[ERROR] Error occurred during setup of VM {vm_name}: {str(e)}\n")
        return None
