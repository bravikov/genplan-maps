# Генпланы России

http://www.genplan-maps.ru/

# Локальный запуск приложения

Запустить сервер для раздачи тайлов:

```bash
cd local-maps
python3 -m http.server 8001
```

В папке local-maps должны быть карты.

Перед запуском приложения нужно настроить окружение:

```bash
cd genplan-maps
source .local_env
```

Запустить приложение:

```bash
cd genplan-maps
gunicorn -b 0.0.0.0:8002 system.wsgi
```

Запустите браузер на той же машине, где запущено приложение и введите адрес:

```
http://localhost:8002/
```

Если ваш смартфон находится в той же локальной сети, что и машина, где запущено приложение, то можно открыть приложение в браузере на смартфоне с помощью адреса:

```
http://192.168.1.101:8002/
```

Где 192.168.1.101 — IP-адрес машины, на которой запущено приложение.

# Карты

Публикация карт в Яндекс Облако:

```
cd local-maps
aws --endpoint-url=https://storage.yandexcloud.net s3 cp --recursive gelendzhik-maps s3://genplan-maps/gelendzhik-maps
```

# Разработка

Сайт сделан на Django.

Движок карты написан на JavaScript. Движок расположен в папке genplan/static/engine.
