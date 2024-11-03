from auth import get_token

from utils.cluster_mng import create_cluster
from utils.ansible_mng import run_playbook

from api.ssh_key_mng import upload_ssh_key_to_vm
from api.vm_mng import reinstall_os

from config import API_KEY

if __name__ == '__main__':
    # Ключ доступа к API из админки NetAngels
    api_token = get_token(API_KEY)
    # Эталонный образ используемый в инфраструктуре
    golden_img = 'img_debian-bookworm'
    # Тип среды
    env_type = 'tst'
    # Тарифы по умолчанию
    tariff_nvme = 'tiny' # Тарифы (tiny, small, medium, large и другие) имееют NVMe диски

    # Создание кластера из 3 мастер-нод и 2 клиентов в среде tst
    # create_cluster(api_token, 3, 2, tariff_nvme, golden_img, env_type)
    # run_playbook(env_type, 'consul_nomad_setup')

    # Для чистого теста
    srv_one_name = 'srv-node-01'
    srv_two_name = 'srv-node-02'
    srv_three_name = 'srv-node-03'
    srv_four_name = 'cli-node-01'
    srv_five_name = 'cli-node-02'

    reinstall_os(api_token, srv_one_name, golden_img)
    reinstall_os(api_token, srv_two_name, golden_img)
    reinstall_os(api_token, srv_three_name, golden_img)
    reinstall_os(api_token, srv_four_name, golden_img)
    reinstall_os(api_token, srv_five_name, golden_img)

    upload_ssh_key_to_vm(api_token, srv_one_name)
    upload_ssh_key_to_vm(api_token, srv_two_name)
    upload_ssh_key_to_vm(api_token, srv_three_name)
    upload_ssh_key_to_vm(api_token, srv_four_name)
    upload_ssh_key_to_vm(api_token, srv_five_name)

    run_playbook(env_type, 'consul_nomad_setup')