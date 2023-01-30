# Test task, Socketio chat + FastAPI REST
## Реализовано:

 - Базовые методы API с аутентификацией и авторизацией через OAuth2 + JWT
 - Загрузка, кроп и сохранение картинок в БД
 - Методы работы с чатами: создание,удаление
 - Частичный функционал чатов на SocketIO (один сокет сервера для обработки сообщений, вступления в чаты)
 - Тестирование методов авторизации с помощью Pytest
 - Контейнеризация БД и АПИ
 - Кастомный сваггер

## Можно реализовать:
 - Работу чата на websockets (из коробки FastAPI)
 - Конфигурационные файлы (деплой, локальная сборка)
 - Большее покрытие тестами + тесты сокетов
 - Примонтировать сокеты к веб-приложению (у меня не получилось)
 - Конфигурационные файлы для Kuber (Ansible playbook (?))
 - Кастомное логгирование

## Запуск
docker compose build && docker compose up 

(не смог обернуть сервер сокета в контейнер, оставил комментарий)