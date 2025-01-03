import os
import subprocess
from api.net_mng import get_vm_lan_ip

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

# Определяем путь к файлу инвентаря на основе типа среды
def get_inventory_path(env_type):
    valid_env_types = {'tst', 'dev', 'stg', 'prd'}
    print(f"[INFO] Fetching inventory path for environment: {env_type}")

    if env_type not in valid_env_types:
        print("[ERROR] Inventory file is not defined. Make sure environment type is one of the following: tst, dev, stg, prd")
        return None

    inventory_file = f'{env_type}.ini'
    inventory_path = os.path.join(project_root, f'ansible/inventory/{inventory_file}')
    print(f"[INFO] Inventory path: {inventory_path}")
    return inventory_path

def update_inventory(api_token, vm_name, vm_ip, vm_type, env_type):
    # print(f"\n[INFO] Updating inventory for VM: {vm_name}, IP: {vm_ip}, Type: {vm_type}, Environment: {env_type}")
    print(f"\n[INFO] Updating inventory for VM: {vm_name}, Type: {vm_type}, Environment: {env_type}")

    inventory_path = get_inventory_path(env_type)
    if not inventory_path:
        print(f"[ERROR] Invalid environment type specified: {env_type}. Skipping inventory update.")
        return
    
    vm_lan_ip = get_vm_lan_ip(api_token, vm_name)
    section = f"nomad_consul_{vm_type}s"
    # entry = f'{vm_name} ansible_host={vm_ip} internal_ip={vm_lan_ip}\n'
    entry = f'{vm_name} internal_ip={vm_lan_ip}\n'

    print(f"[DEBUG] Inventory entry to add: {entry.strip()}")
    
    # Проверка существования файла и создание, если необходимо
    if not os.path.exists(inventory_path):
        print(f"[INFO] Inventory file {inventory_path} does not exist. Creating new file.")
        with open(inventory_path, 'w') as file:
            file.write(f"[{section}]\n")
    
    # Проверка и добавление записи в инвентарь
    with open(inventory_path, 'r+') as file:
        inventory_contents = file.readlines()
        section_found = False
        entry_found = False
        
        # Поиск раздела и записи
        for line in inventory_contents:
            if line.strip() == f'[{section}]':
                section_found = True
            if entry.strip() == line.strip():
                entry_found = True
                break
        
        # Добавление записи или раздела
        if section_found and not entry_found:
            print(f"[INFO] Section [{section}] found, but entry not present. Adding entry to inventory.")
            file.write(entry)
        elif not section_found:
            print(f"[INFO] Section [{section}] not found. Adding section and entry to inventory.")
            file.write(f'\n[{section}]\n')
            file.write(entry)
        else:
            print(f"[INFO] Entry for {vm_name} already exists in inventory. No update required.")

def run_playbook(env_type, name_playbook):
    inventory_path = get_inventory_path(env_type)
    if not inventory_path:
        print(f"[ERROR] Invalid environment type specified: {env_type}. Cannot run playbook.")
        return

    playbook_path = os.path.join(project_root, f'ansible/playbooks/{name_playbook}.yml')
    print(f"[INFO] Running playbook: {name_playbook}, Inventory: {inventory_path}")

    try:
        # Запуск плейбука
        subprocess.run(["ansible-playbook", "-i", inventory_path, playbook_path], check=True)
        print(f"[SUCCESS] Playbook {name_playbook} completed successfully using inventory from {inventory_path}.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Playbook execution failed: {name_playbook}. Error: {e}")
    except FileNotFoundError:
        print(f"[ERROR] Playbook {playbook_path} or inventory file {inventory_path} not found.")
