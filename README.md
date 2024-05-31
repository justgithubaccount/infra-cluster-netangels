# ff-consul-nomad
> **Крайне черновой вариант!** 
> 
> Переделаю доку позже, пока в паблике пусть повисит (так и было задуманно). Мб уйдут в локалку за nat... была бы не плохо более безопасней конечно сделать... главно в каком-то виде было займеить рабочий плейбук и конфиги которые потом можно использовать и воспроизвести где угодно...
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
> Питоновские обертки для хостинга NetAngels (vds), какие-то куски ансибла взяты отсюда - [snowsync-cfg-tst](https://gitlab.com/justgitlabaccount/snowsync-cfg-tst)

# Задание
Собрать тестовый Сonsul + Nomad кластер (3 ноды) внутри в контейнере запустить nginx который показывает строку **«Mission Complete!»**  

# Next
- по сути у меня есть тоже самое для кубика, нужно протестить как будет работать [тг-вэб апп](https://gitlab.com/justgitlabaccount/snowsync-cfg-tst) в номаде + консул + остальные продукты хашикорпов ваулт тот же. Изначально думал затестить его в кубике, но номад больше привлекал, благодаря одной [статье](https://habr.com/ru/articles/445030/).
- **использовать jinja2** в питоне (формировать конфиги)
- ...

# welcome-consul
**Вэбка консула** - http://80.87.104.168:8500/ui/  
**Собрать все ноды в кластер**  
```consul join 192.168.0.2 192.168.0.3 192.168.0.4```  
**Проверить состояние Consul кластера**  
```consul members```  
```consul operator raft list-peers```  
**Зарегать сервис в консуле**  
```consul services register nginx.json```

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
**Проверить логи номада, докера, консула**  
```journalctl -u nomad -f```  
```journalctl -u docker -f```  
```journalctl -u consul -f```  
**Службы**  
```systemctl status nomad```  
```systemctl status docker```  
```systemctl status consul```  
# NOMAD Task
**Запуск задания**  
```nomad job run nginx.nomad```    
**Проверить**  
```nomad job status nginx```  
### nginx.nomad
```
job "nginx" {
  datacenters = ["dc1"] # Указывает датацентр, в котором будет выполняться задание

  group "nginx" {
    count = 3 # Определяет количество экземпляров группы задач

    task "nginx" {
      driver = "docker" # Указывает, что для выполнения задачи используется Docker

      config {
        image = "nginx:latest" # Используемый образ Docker
        ports = ["http"] # Определяет порт с меткой "http", который будет открыт в контейнере
        force_pull = false # Указывает, что образ не будет загружаться повторно, если он уже есть локально
        volumes = [
          "local/index.html:/usr/share/nginx/html/index.html" # Монтирует файл local/index.html в контейнер
        ]
      }

      template {
        data = <<-EOF
        Mission Complete!
EOF
        destination = "local/index.html" # Путь, куда будет записан файл
      }

      resources {
        cpu    = 500
        memory = 256
      }

      # Регистрация сервиса в Consul
      service {
        name = "nginx" # Имя сервиса в Consul
        port = "http"  # Порт, который будет зарегистрирован в Consul

        check {
          name     = "nginx HTTP check" # Имя проверки состояния
          type     = "http"             # Тип проверки - HTTP
          path     = "/"                # Путь для HTTP-запроса проверки состояния
          interval = "10s"              # Интервал между проверками - 10 секунд
          timeout  = "2s"               # Таймаут для каждой проверки - 2 секунды
        }
      }

      env {
        NGINX_ROOT = "/usr/share/nginx/html" # Переменная окружения, указывающая на корневую директорию nginx
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
# Misc 
**Зеркала для докера**  
```sudo sh -c 'echo "{"registry-mirrors": ["https://mirror.gcr.io", "https://daocloud.io", "https://c.163.com/", "https://huecker.io/", "https://registry.docker-cn.com"]}" >> /etc/docker/daemon.json'```

# Docs
[Drivers: Docker | Nomad | HashiCorp Developer](https://developer.hashicorp.com/nomad/docs/drivers/docker#plugin-options)  
[plugin Block - Agent Configuration | Nomad | HashiCorp Developer](https://developer.hashicorp.com/nomad/docs/configuration/plugin)  

# Errors
Multiple private IPv4 addresses found. Please configure one with 'bind' and/or 'advertise'.  
...