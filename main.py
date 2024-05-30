from auth import get_token

from utils.ansible_mng import run_playbook
from utils.vm_setup import setup_vm
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

    srv_one_name = 'node-01' # Имя сервера (в вэбке), hostname будет вида vm_73ca5cbf
    srv_two_name = 'node-02' # ...
    srv_three_name = 'node-03' # ...

    # # Сервера для кластера
    # srv_one_vm = setup_vm(api_token, srv_one_name, tariff_nvme, 10, golden_img, False, env_type) 
    # srv_two_vm = setup_vm(api_token, srv_two_name, tariff_nvme, 10, golden_img, False, env_type)
    # srv_three_vm = setup_vm(api_token, srv_three_name, tariff_nvme, 10, golden_img, False, env_type)

    # # Запуск плейбука после того как сервера будут готовы
    # if srv_one_vm and srv_two_vm and srv_three_vm:
    #     run_playbook(env_type, 'consul_nomad_setup')

    ### Для чистого теста
    reinstall_os(api_token, srv_one_name, golden_img)
    reinstall_os(api_token, srv_two_name, golden_img)
    reinstall_os(api_token, srv_three_name, golden_img)

    upload_ssh_key_to_vm(api_token, srv_one_name)
    upload_ssh_key_to_vm(api_token, srv_two_name)
    upload_ssh_key_to_vm(api_token, srv_three_name)

    run_playbook(env_type, 'consul_nomad_setup')