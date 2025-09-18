
```markdown
# Page Analyzer

Инструмент для быстрого и комплексного анализа веб-страниц.

---

## В проекте используются технологии

- **Flask (3.0.2)** — Фреймворк для разработки веб-приложений на Python  
- **Gunicorn (20.1.0)** — WSGI-сервер для запуска Flask-приложений в продакшене  
- **Bootstrap** — CSS-фреймворк для создания пользовательского интерфейса  
- **BeautifulSoup** — Библиотека для парсинга HTML и XML документов  
- **python-dotenv (1.0.1)** — Загрузка конфигурационных переменных из `.env`  
- **PostgreSQL (16.10)** — Система управления реляционными базами данных  
- **ruff (0.12.7)** — Линтер  
- **Docker** — Создание, развертывание и управление изолированными контейнерами с приложением и его зависимостями

---

## Установка

1. Склонируйте репозиторий:
```bash
git clone git@github.com:lisaCookie/python-project-83.git
```

2. Перейдите в папку:
```bash
cd python-project-83
```

3. Создайте базу данных:
```bash
psql -U <имя_пользователя> -d <имя_базы> -f database.sql
```

4. В директории `page_analyzer` создайте файл `.env` и настройте параметры:
```env
DATABASE_URL=postgresql://{username}:{password}@{host}:{port}/{databasename}
SECRET_KEY='{your secret key}'
```

---

## Запуск

- Установить зависимости:
```bash
make install
```

- Для разработки:
```bash
make dev
```

- Для сборки:
```bash
make build
```

- Для деплоя:
```bash
make start
```

---

## Статус тестирования и линтинга

[![Actions Status](https://github.com/lisaCookie/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/lisaCookie/python-project-83/actions)
[![Python CI](https://github.com/lisaCookie/python-project-83/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/lisaCookie/python-project-83/actions/workflows/ci.yml)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=lisaCookie_python-project-83&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=lisaCookie_python-project-83)

---


- [Локальный запуск](http://127.0.0.1:5500/index.html)  
- [Продакшн-сервер](https://python-project-83-tc5z.onrender.com)
```

---
