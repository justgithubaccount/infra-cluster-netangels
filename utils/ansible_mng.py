import os
import subprocess

from api.net_mng import get_vm_lan_ip

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

# Определяем путь к файлу инвентаря на основе типа среды
def get_inventory_path(env_type):
    valid_env_types = {'tst', 'dev', 'stg', 'prd'}

    if env_type not in valid_env_types:
        print('Inventory file is not defined. Make sure environment type is one of following: tst, dev, stg, prd')
        return None

    inventory_file = f'{env_type}.ini'
    return os.path.join(project_root, f'ansible/inventory/{inventory_file}')

def update_inventory(api_token, vm_name, vm_ip, vm_type, env_type):
    print(f"update_inventory called with: vm_name={vm_name}, vm_ip={vm_ip}, vm_type={vm_type}, env_type={env_type}")
    inventory_path = get_inventory_path(env_type)
    vm_lan_ip = get_vm_lan_ip(api_token, vm_name)
    section = f"nomad_consul_{vm_type}s"

    # Проверка существования файла и создание, если необходимо
    if not os.path.exists(inventory_path):
        with open(inventory_path, 'w') as file:
            file.write(f"[{section}]\n")
    
    # Проверяем, есть ли уже такая запись
    with open(inventory_path, 'r+') as file:
        inventory_contents = file.readlines()
        entry = f'{vm_name} ansible_host={vm_ip} internal_ip={vm_lan_ip}\n'
        section_found = False
        entry_found = False
        
        # Проверяем, существует ли раздел и запись
        for line in inventory_contents:
            if line.strip() == f'[{section}]':
                section_found = True
            if entry.strip() == line.strip():
                entry_found = True
                break
        
        # Если раздел найден, но запись отсутствует, добавляем запись
        if section_found and not entry_found:
            file.write(entry)
        # Если раздел не найден, добавляем раздел и запись
        elif not section_found:
            file.write(f'\n[{section}]\n')
            file.write(entry)

def run_playbook(env_type, name_playbook):
    inventory_path = get_inventory_path(env_type)

    # Определение полного пути к плейбуку
    playbook_path = os.path.join(project_root, f'ansible/playbooks/{name_playbook}.yml')

    try:
        # Запуск плейбука с использованием указанного файла инвентаря
        subprocess.run(["ansible-playbook", "-i", inventory_path, playbook_path], check=True)
        print(f"Playbook {name_playbook} completed successfully using inventory from {inventory_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running playbook {name_playbook}:", e)
    except FileNotFoundError:
        print(f"Playbook {playbook_path} or inventory file {inventory_path} not found.")
