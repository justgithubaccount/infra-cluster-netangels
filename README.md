# ff-consul-nomad
> v0.1.1 alpha - рефакторинг роли консула, добавлена функция по получения локального айпи адреса, переделанна логика формирования инветори файла под кластер, сам процесс разворачивая обернут в функцию, другие мелкие правки...
> 
> v0.0.2 alpha - nginx как сервис отображается в вэбке консула на 3 нодах
> 
> v0.0.1 alpha - закомичен чтобы сохранить промежуточный этап, где поднят кластер номада и на всех нодах отдается «Mission Complete!» (без Консула) 

# Задание
Изначально тестовое задание звучало так: Собрать тестовый Сonsul + Nomad кластер (3 ноды) внутри в контейнере запустить nginx который показывает строку **«Mission Complete!»**  

# Next
- по сути у меня есть тоже самое для кубика, нужно протестить как будет работать [тг-вэб апп](https://gitlab.com/justgitlabaccount/snowsync-cfg-tst) в номаде + консул + остальные продукты хашикорпов ваулт тот же. Изначально думал затестить его в кубике, но номад больше привлекал, благодаря одной [статье](https://habr.com/ru/articles/445030/).
- **использовать jinja2** в питоне (формировать конфиги)
- оптимизировать код питона
- накинуть логики на ансибл
- прокомментировать
- ...

# welcome-consul
**Вэбка консула** - http://80.87.104.168:8500/ui/  
**Собрать все ноды в кластер**  
```consul join 192.168.0.1 192.168.0.2 192.168.0.3```  
**Проверить состояние Consul кластера**  
```consul members```  
```consul operator raft list-peers```  
```consul info```  
```journalctl -u consul -xe```  
```systemctl status consul```  
```curl http://127.0.0.1:8500/v1/catalog/nodes```  
```curl http://127.0.0.1:8500/v1/catalog/services```  

# welcome-nomad
**Вэбка номада** - http://80.87.104.168:4646/ui/jobs  
**Собрать все ноды в кластер**     
```nomad server join 192.168.0.2 192.168.0.3 192.168.0.4```  
**Проверить состояние Nomad кластера**  
```nomad server members```  
```nomad node status```  
```nomad node status -self```  
**Проверить плагин докера**  
```nomad node status -self -verbose | grep docker```    
**Проверить логи номада, докера**  
```journalctl -u nomad -f```  
```journalctl -u docker -f```  
**Службы**  
```systemctl status nomad```  
```systemctl status docker```  
# NOMAD Task
**Запуск задания**  
```nomad job run nginx.nomad```    
**Проверить**  
```nomad job status nginx```  

# Misc 
**Зеркала для докера**  
```sudo sh -c 'echo "{"registry-mirrors": ["https://mirror.gcr.io", "https://daocloud.io", "https://c.163.com/", "https://huecker.io/", "https://registry.docker-cn.com"]}" >> /etc/docker/daemon.json'```

# Docs
[Drivers: Docker | Nomad | HashiCorp Developer](https://developer.hashicorp.com/nomad/docs/drivers/docker#plugin-options)  
[plugin Block - Agent Configuration | Nomad | HashiCorp Developer](https://developer.hashicorp.com/nomad/docs/configuration/plugin)  

# Errors
Nomad - Multiple private IPv4 addresses found. Please configure one with 'bind' and/or 'advertise'.  
Consul - [DEBUG] agent.server.cert-manager: CA has not finished initializing  
Consul - [WARN]  agent.server.raft: no known peers, aborting election