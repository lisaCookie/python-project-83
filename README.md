Page Analizer
Инструмент для быстрого и комплексного анализа веб-страниц

В проекте используются технологии:

Flask(3.0.2)           Фреймворк для разработки веб-приложений на Python
Gunicorn(20.1.0)       WSGI-сервер для запуска Flask-приложений в продакшене
Bootstrap              CSS-фреймворк для создания пользовательского интерфейса 
BeautifulSoup          Библиотека для парсинга HTML и XML документов
python-dotenv(1.0.1)   Загрузка конфигурационных переменных из .env
PostgreSql(16.10)      Система управления реляционными базами данных
ruff(0.12.7)           Линтер
Docker                 Cоздание, развертывание и управление изолированными контейнерами 
                       с приложением и его зависимостями


Установка

Склонировать репозиторий
git clone git@github.com:lisaCookie/python-project-83.git

Перейти в папку
cd python-project-83

Создать базу данных
psql -U имя_пользователя -d имя_базы -f database.sql

Создайте в директории page_analyzer файл .env и настройте параметры
DATABASE_URL=postgresql://{username}:{password}@{host}:{port}/{databasename}
SECRET_KEY='{your secret key}'


Запуск

Установить зависимости
make install

Разработка
make dev

Сборка
make build 

Деплой
make start


### Hexlet tests and linter status:
[![Actions Status](https://github.com/lisaCookie/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/lisaCookie/python-project-83/actions)
[![Python CI](https://github.com/lisaCookie/python-project-83/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/lisaCookie/python-project-83/actions/workflows/ci.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=lisaCookie_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=lisaCookie_python-project-83)

http://127.0.0.1:5500/index.html
https://python-project-83-tc5z.onrender.com
