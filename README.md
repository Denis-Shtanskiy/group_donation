# __Тестовое задание BackendProninTeam__

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## Использованные при реализации проекта технологии
 - Python
 - Django
 - djangorestframework
 - Nginx
 - Docker
 - PostgreSQL
 - Celery
 - Redis

## __Как развернуть проект__

### Для установки проекта потребуется выполнить следующие действия:

_Локальная настройка и запуск проекта_

Клонировать репозиторий к себе на компьютер и перейти в директорию с проектом:
```bash
git clone https://github.com/Denis-Shtanskiy/group_donation.git
cd group_donation
```
Для проекта создать и активировать виртуальное окружение, установить зависимости:
__для windows:__
```bash
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
cd group_donations
```
__для linux:__
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
cd group_donations
```
### .env
Для корректной работы backend-части проекта, создайте в корне файл `.env` и заполните его переменными по примеру из файла `.env.example` или по примеру ниже:
```bash
POSTGRES_DB=postgresdb
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
DB_HOST=db
DB_PORT=5432
SECRET_KEY='django-insecure-secret-secret-key'       # стандартный ключ, который создается при старте проекта
DEBUG=True
ALLOWED_HOSTS=IP_адрес_сервера, 127.0.0.1, localhost, домен_сервера      # если используется сервер и домен
PROJECT_EMAIL=any_project_email@example.com      # email проекта с которого будут отправляться письма юзерам
REDIS_HOST=redis
REDIS_PORT=6379
SUPERUSER_USERNAME=AdminDonations       # переменные для автоматического создания суперюзера,
SUPERUSER_PASSWORD=donations12345       # если не указать, применятся стандартные из скрипта
SUPERUSER_EMAIL=admin@nothing.not      # вид стандартных переменных ('admin', 'admin@example.com, 'admin12345')
```

Установите [docker compose](https://www.docker.com/) на свой компьютер.
Для запуска проекта на локальной машине достаточно:
* Запустить проект, ключ `-d` запускает проект в фоновом режиме
* выполнить миграции
* запустить скрипт создания суперюзера
* запустить менеджмент команду для загрузки базы моковыми данными,
либо базовую команду, для загрузки действительных данных.
```bash
docker compose up -d --build
docker compose exec backend python manage.py migrate
docker compose exec backend bash create_superuser_script.sh
docker compose exec backend python manage.py mock_data <count>     # число необходимых моковых данных при больших количествах потребуется время
docker compose exec backend manage.py example_import <путь до файла CSV>/example.csv     # при имеющемся файле CSV можно заполнить базу из файла по его названию
```

#### Автор
Denis Shtanskiy
Telegram: @shtanskiy
