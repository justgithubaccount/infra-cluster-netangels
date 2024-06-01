from utils.vm_setup import setup_vm
from utils.ansible_mng import run_playbook, update_inventory

def create_cluster(api_token, num_servers, num_clients, tariff_nvme, golden_img, env_type):
    server_names = [f'srv-node-{i+1:02d}' for i in range(num_servers)]
    client_names = [f'cli-node-{i+1:02d}' for i in range(num_clients)]

    for server_name in server_names:
        vm = setup_vm(api_token, server_name, tariff_nvme, 10, golden_img, False)
        if vm:
            print(f"Updating inventory for server: {server_name} with IP: {vm['main_ip']}, env_type: {env_type}")
            update_inventory(api_token, server_name, vm['main_ip'], 'server', env_type)

    for client_name in client_names:
        vm = setup_vm(api_token, client_name, tariff_nvme, 10, golden_img, False)
        if vm:
            print(f"Updating inventory for client: {client_name} with IP: {vm['main_ip']}, env_type: {env_type}")
            update_inventory(api_token, client_name, vm['main_ip'], 'client', env_type)

    # Запуск плейбука после того как сервера будут готовы
    if all(server_names) and all(client_names):
        run_playbook(env_type, 'consul_nomad_setup')
