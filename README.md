# ff-consul-nomad
> v0.2.1 - отладка  
> v0.2.0 - рефакторинг роли номада, установка кластера с нужным кол-вом серверов (мастер/слейв), общие правки  
> v0.1.1 - рефакторинг роли консула, добавлена функция по получения локального айпи адреса, переделанна логика формирования инветори файла под кластер, сам процесс разворачивая обернут в функцию, другие мелкие правки...  
> v0.0.2 - nginx как сервис отображается в вэбке консула на 3 нодах  
> v0.0.1 - закомичен чтобы сохранить промежуточный этап, где поднят кластер номада и на всех нодах отдается «Mission Complete!» (без Консула) 

# Запуск
```/home/jenya/ff-consul-nomad/ansible/inventory/tst.ini``` # Очистить инвентори файл, если не пустой  
```export ANSIBLE_ROLES_PATH=/home/jenya/ff-consul-nomad/ansible/roles``` # Добавить энву до директории с ролями  
```(venv) jenya@windows:~/ff-consul-nomad/ansible$ ../venv/bin/python ../main.py``` # One-Click Install  
```(venv) jenya@windows:~/ff-consul-nomad/ansible$ ansible-playbook -i inventory/tst.ini playbooks/consul_nomad_setup.yml -v``` # Запуск плейбука отдельно (если после установки серверов плейбук не запустился) | может произойти

**Вэбка консула** - http://ip-srv:8500/ui/  
**Вэбка номада** - http://ip-srv:4646/ui/  
