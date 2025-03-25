### Hexlet tests and linter status:
[![Actions Status](https://github.com/Gamabyta24/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Gamabyta24/python-project-52/actions)
# Task Manager

Task Manager – это система управления задачами, аналогичная [Redmine](http://www.redmine.org/). Приложение позволяет создавать задачи, назначать исполнителей и изменять их статусы. Для работы с системой требуется регистрация и аутентификация.

## Функциональность
- Регистрация и аутентификация пользователей
- Создание, редактирование и удаление задач
- Назначение исполнителей на задачи
- Управление статусами задач
- Просмотр списка задач и деталей по каждой задаче

## Технологии
- Python
- Django
- Bootstrap
- PostgreSQL

## Установка и запуск

### Локальный запуск

1. Клонируйте репозиторий:
   ```sh
   git clone https://github.com/Gamabyta24/python-project-52.git
   cd python-project-52
   ```
2. Установите [uv](https://docs.astral.sh/uv/#installation):
   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh # Для Linux/macOS
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" # Для Windows
   ```
2. Создайте и активируйте виртуальное окружение:
   ```sh
   uv venv
   source venv/bin/activate  # Для Linux/macOS
   venv\Scripts\activate  # Для Windows
   ```
3. Установите зависимости:
   ```sh
   pip install -r requirements.txt
   ```
4. Примените миграции:
   ```sh
   python manage.py migrate
   ```
5. Запустите сервер:
   ```sh
   python manage.py runserver
   ```

Приложение будет доступно по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).


## Развертывание
Приложение можно развернуть на любой платформе, поддерживающей Django и PostgreSQL. Я развернул приложение на платформе render.com.

Ссылка: https://python-project-52-yt5k.onrender.com



## Автор
Разработчик: [Gamabyta24](https://github.com/Gamabyta24)



