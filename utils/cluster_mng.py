from utils.vm_setup import setup_vm
from utils.ansible_mng import run_playbook, update_inventory

def create_cluster(api_token, num_servers, num_clients, tariff_nvme, golden_img, env_type):
    print(f"\n--- Starting cluster creation ---")
    print(f"Environment: {env_type}, Number of servers: {num_servers}, Number of clients: {num_clients}")
    print(f"VM Configuration: Tariff: {tariff_nvme}, Image: {golden_img}")

    # Generate server and client names
    server_names = [f'srv-node-{i+1:02d}' for i in range(num_servers)]
    client_names = [f'cli-node-{i+1:02d}' for i in range(num_clients)]

    # Create servers and update inventory
    for server_name in server_names:
        print(f"\n[INFO] Setting up server VM: {server_name}")
        vm = setup_vm(api_token, server_name, tariff_nvme, 10, golden_img, False, env_type)
        if vm:
            print(f"[INFO] Updating inventory for server: {server_name} with IP: {vm['main_ip']}")
            update_inventory(api_token, server_name, vm['main_ip'], 'server', env_type)
        else:
            print(f"[WARNING] Setup failed for server: {server_name}. Skipping inventory update.")

    # Create clients and update inventory
    for client_name in client_names:
        print(f"\n[INFO] Setting up client VM: {client_name}")
        vm = setup_vm(api_token, client_name, tariff_nvme, 10, golden_img, False, env_type)
        if vm:
            print(f"[INFO] Updating inventory for client: {client_name} with IP: {vm['main_ip']}")
            update_inventory(api_token, client_name, vm['main_ip'], 'client', env_type)
        else:
            print(f"[WARNING] Setup failed for client: {client_name}. Skipping inventory update.")

    # Run playbook after all VMs are ready
    # print("\n[INFO] Running playbook to set up Consul and Nomad on the cluster")
    # try:
    #     run_playbook(env_type, 'consul_nomad_setup')
    #     print("[SUCCESS] Playbook execution completed.")
    # except Exception as e:
    #     print(f"[ERROR] Playbook execution failed: {str(e)}")

    print(f"--- Cluster creation completed for environment: {env_type} ---\n")
