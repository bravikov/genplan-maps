# Генпланы России

https://genplan-maps.ru/

# Разворачивание Docker-контейнера

```bash
cd genplan-maps
docker build -t genplan-maps .
docker run -d -v "$PWD":/usr/src/app -p 443:8001 genplan-maps
```

# Локальный запуск приложения

## Установка зависимостей на macOS

```bash
brew install postgresql
pip3 install -r requirements.txt
```

Запустить сервер для раздачи тайлов:

```bash
cd local-maps
python3 -m http.server 8001
```

В папке local-maps должны быть карты (папки с тайлами). Пример структуры папок:

    local-maps
        genplan-maps
            kazan
            krasnodar
            ...

Перед дальнейшим запуском приложения нужно настроить окружение:

```bash
cd genplan-maps
source .local_env
```

В .local_env нужно указать свой IP-адрес в MAPS_STORAGE.

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
cd local-maps/genplan-maps
aws --endpoint-url=https://storage.yandexcloud.net s3 cp --recursive gelendzhik-maps s3://genplan-maps/gelendzhik-maps
```

# Разработка

Сайт сделан на Django.

Движок карты написан на JavaScript. Движок расположен в папке genplan/static/engine.
