from api.vm_mng import create_vm, is_vm_ready
from api.net_mng import add_to_local_net

from utils.ansible_mng import update_inventory

def setup_vm(token, vm_name, vm_tariff, vm_disk_size, vm_image, is_backup_enabled):
    try:
        vm_data = create_vm(token, vm_name, vm_tariff, vm_disk_size, vm_image, is_backup_enabled)

        vm_id = vm_data['id']
        vm_name = vm_data['name']
        vm_uid = vm_data['uid']
        vm_ip = vm_data['main_ip']

        print("Start building VM")
        print(f"ID - {vm_id}")
        print(f"Name (web) - {vm_name}")
        print(f"UID (host) - {vm_uid}")
        print(f"IP - {vm_ip}")

        if is_vm_ready(token, vm_id):  # Проверяем, готова ли VM
            add_to_local_net(token, vm_name)
            # update_inventory(token, vm_name, vm_ip, env_type)  # Обновляем инветори файл
            return vm_data
        else:
            print("VM is not ready in specified timeout")
            return None
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None