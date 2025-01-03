from auth import get_token
from utils.cluster_mng import create_cluster
from utils.ansible_mng import run_playbook
from api.ssh_key_mng import upload_ssh_key_to_vm
from api.vm_mng import reinstall_os
from config import API_KEY_NETANGELS, MASTER_COUNT, CLIENT_COUNT # Переделать (что если будет 100 енвов будет?)

# Настройки по умолчанию
golden_img = 'img_debian-bookworm'
env_type = 'tst'
tariff_nvme = 'tiny'

def deploy_cluster(api_token, num_servers=MASTER_COUNT, num_clients=CLIENT_COUNT):
    """Развертывание нового кластера с заданным количеством серверов и клиентов"""
    print(f"[INFO] Starting deployment of new cluster with {num_servers} servers and {num_clients} clients.")
    create_cluster(api_token, num_servers, num_clients, tariff_nvme, golden_img, env_type)
    # run_playbook(env_type, 'consul_nomad_setup')
    print("[SUCCESS] Cluster deployment completed.")

def redeploy_cluster(api_token, server_names, client_names):
    """Повторная установка ОС на указанных серверах и загрузка SSH-ключа"""
    print("[INFO] Starting redeployment of existing cluster nodes.")
    
    # Повторная установка ОС на серверах
    for vm_name in server_names + client_names:
        print(f"[INFO] Reinstalling OS on VM: {vm_name}")
        reinstall_os(api_token, vm_name, golden_img)
        upload_ssh_key_to_vm(api_token, vm_name)
    
    # Повторный запуск playbook
    run_playbook(env_type, 'consul_nomad_setup')
    print("[SUCCESS] Cluster redeployment completed.")

if __name__ == '__main__':
    # Ключ доступа к API
    api_token = get_token(API_KEY_NETANGELS)

    # Вызов функций развертывания или переустановки кластера
    # Пример для развертывания нового кластера
    deploy_cluster(api_token)

    # Пример для переустановки существующего кластера
    # server_names = ['srv-node-01', 'srv-node-02', 'srv-node-03']
    # client_names = ['cli-node-01', 'cli-node-02']
    # redeploy_cluster(api_token, server_names, client_names)
