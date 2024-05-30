# ff-consul-nomad
> **Крайне черновой вариант!** 
> 
> Переделаю всё позже, пока так и в паблике пусть повисит (так и было задуманно). Мб уйдут в локалку за nat... была бы не плохо более безопасней конечно сделать... главно в каком-то виде было займеить рабочий плейбук и конфиги которые потом можно использовать и воспроизвести где угодно...
> 
> Первый коммит (v0.0.1 alpha): закомичен чтобы сохранить промежуточный этап, где поднят кластер номада и на всех нодах отдается «Mission Complete!» (без Консула) 
>
> Второй коммит (v0.0.2 alpha): nginx как сервис отображается в вэбке консула на 3 нодах
> http://80.87.104.168:8500/ui/dc1/services/nginx/instances  
>
> http://80.87.104.168:8080/  
> http://80.87.104.39:8080/  
> http://80.87.104.143:8080/  
>
> Осталось ~~добавить консул~~ и отладить плейбуки (роли, таски в ролях), сейчас плейбук поднимает кластер номада и консула с регистрацией нджикса в консуле, без вываливания в ошибку
> Питоновские обертки для хостинга (vds), какие-то куски ансибла взяты отсюда - https://gitlab.com/justgitlabaccount/snowsync-cfg-tst

# задание такое 
собрать тестовый consul+nomad кластер (из 3 слабых нод)
внутри в контейнере запустить nginx  который показывает строку «Mission Complete!»

# welcome-consul
**Собрать все ноды в кластер**  
```consul join 192.168.0.2 192.168.0.3 192.168.0.4```  
**Проверить состояние Consul кластера**  
```consul members```  
```consul operator raft list-peers```  

**Вэбка консула** - http://80.87.104.168:8500/ui/  

# welcome-nomad
**Собрать все ноды в кластер**     
```nomad server join 192.168.0.2 192.168.0.3 192.168.0.4```  
**Проверить состояние Nomad кластера**  
```nomad server members```  
```nomad node status```  
```nomad node status -self```  
**Проверить плагин докера**  
```nomad node status -self -verbose | grep docker```  

[Drivers: Docker | Nomad | HashiCorp Developer](https://developer.hashicorp.com/nomad/docs/drivers/docker#plugin-options)  
[plugin Block - Agent Configuration | Nomad | HashiCorp Developer](https://developer.hashicorp.com/nomad/docs/configuration/plugin)  

**Службы**  
```systemctl status nomad```    

**Проверить логи номада и докера**  
```journalctl -u nomad -f```  
```journalctl -u docker -f```  
journalctl -u consul -f


**Вэбка номада** - http://80.87.104.168:4646/ui/jobs  

# CONSUL Services
### nginx.json (сервис)  

```{
  "service": {
    "name": "nginx",
    "tags": ["web"],
    "port": 80
  }
}
```

Зарегать сервис nginx.json в консуле  
consul services register nginx.json  

# NOMAD tasks
### nginx.nomad
```
job "nginx" {
  datacenters = ["dc1"]

  group "nginx" {
    count = 3

    task "nginx" {
      driver = "docker"

      config {
        image = "nginx:latest"
        ports = ["http"]
        force_pull = false
        volumes = [
          "local/index.html:/usr/share/nginx/html/index.html"
        ]
      }

      template {
        data = <<-EOF
Mission Complete!
EOF
        destination = "local/index.html"
      }

      resources {
        cpu    = 500
        memory = 256
      }

      env {
        NGINX_ROOT = "/usr/share/nginx/html"
      }
    }

    network {
      port "http" {
        static = 8080
        to = 80
      }
    }
  }
}
```
Запуск задания  
nomad job run nginx.nomad  
Чек  
nomad job status nginx

root@vm-97c3da39:~# usermod -aG docker nomad  
root@vm-97c3da39:~# systemctl restart nomad  

Докер забанили внезапно походу дела  
```sudo sh -c 'echo "{"registry-mirrors": ["https://mirror.gcr.io", "https://daocloud.io", "https://c.163.com/", "https://huecker.io/", "https://registry.docker-cn.com"]}" >> /etc/docker/daemon.json'```

# Errors
Multiple private IPv4 addresses found. Please configure one with 'bind' and/or 'advertise'.
...