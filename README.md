# infra-cluster-netangels
> v0.3.0 - отладка, мелкие правки для дальнейшего зеркалирования с [infra-cluster](https://github.com/justgithubaccount/infra-cluster)  
> v0.2.1 - отладка  
> v0.2.0 - рефакторинг роли номада, установка кластера с нужным кол-вом серверов (мастер/слейв), общие правки  
> v0.1.1 - рефакторинг роли консула, добавлена функция по получения локального айпи адреса, переделанна логика формирования инветори файла под кластер, сам процесс разворачивая обернут в функцию, другие мелкие правки...  
> v0.0.2 - nginx как сервис отображается в вэбке консула на 3 нодах  
> v0.0.1 - закомичен чтобы сохранить промежуточный этап, где поднят кластер номада и на всех нодах отдается «Mission Complete!» (без Консула) 

# Getting Started
curl -sSL https://install.python-poetry.org | python3 -  
poetry install  
poetry env info  
cd ansible  
poetry run python ../main.py  

# Next
Переосмылить функции create_vm + setup_vm | прочекать по зонам отвественности другие функции | добавить модульность init.py | добиться зеркальности с [infra-cluster](https://github.com/justgithubaccount/infra-cluster)  
Отделить ансибл в другую репу [cluster-deploy](https://github.com/justgithubaccount/cluster-deploy) | поресерчить замену ансиблу [?]  
Добавлять [app-gateway](https://github.com/justgithubaccount/app-gateway) после деплоя кластера как +1 клиента кластера  
Разбить докер-компоуз для приложения из [snowsync-cfg-tst](https://gitlab.com/justgitlabaccount/snowsync-cfg-tst/-/blob/main/docker/snowsync-dev/docker-compose.yml?ref_type=heads) в отдельную джоб-репу [cluster-app](https://github.com/justgithubaccount/cluster-app)  
Отдельная репа [cluster-observability](https://github.com/justgithubaccount/cluster-observability) для наблюдение за кластером  
Запустить все шестиренки [app-flow](https://github.com/justgithubaccount/app-flow)  

# Next (RAW)
инфра под кластер деплоится через терраформ в облако/vds хостинг нетанджелс (3 мастера, 5 клиентов) = 8 серверов | без паблик айпи  
допом создается нджикс/траефик как n+1 клиент кластера  
установка кластера кубик/номад  
добавление в кластер джоб-приложения  
добавление в кластер джоб для приложения  
добавления джоб для наблюдения за всем что происходит в кластере (логи, метрики, трейсы)  
[app-flow](https://github.com/justgithubaccount/app-flow) - магия процессов  

# Запуск (old)
```/home/jenya/ff-consul-nomad/ansible/inventory/tst.ini``` # Очистить инвентори файл, если не пустой  
```export ANSIBLE_ROLES_PATH=/home/jenya/ff-consul-nomad/ansible/roles``` # Добавить энву до директории с ролями  
```(venv) jenya@windows:~/ff-consul-nomad/ansible$ ../venv/bin/python ../main.py``` # One-Click Install  
```(venv) jenya@windows:~/ff-consul-nomad/ansible$ ansible-playbook -i inventory/tst.ini playbooks/consul_nomad_setup.yml -v``` # Запуск плейбука отдельно (если после установки серверов плейбук не запустился) | может произойти  

**Вэбка консула** - http://ip-srv:8500/ui/  
**Вэбка номада** - http://ip-srv:4646/ui/  
