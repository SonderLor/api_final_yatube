# Yatube API

API для социальной сети блогов. Позволяет управлять постами, комментариями,
группами и подписками.
Аутентификация реализована через JWT-токены.

## Основные возможности

- Создание/редактирование/удаление постов
- Добавление комментариев к постам
- Управление сообществами (группами)
- Подписки на других пользователей
- Пагинация и поиск
- JWT-аутентификация

## Установка

1. Клонировать репозиторий:

```bash
git clone https://github.com/SonderLor/yatube-api.git
cd yatube-api
```

2. Создать и активировать виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
```

3. Установить зависимости:

```bash
pip install -r requirements.txt
```

4. Выполнить миграции:

```bash
python manage.py migrate
```

5. Запустить сервер:

```bash
python manage.py runserver
```

## Примеры запросов

### Аутентификация

Получение JWT-токена:

```bash
curl -X POST http://localhost:8000/api/v1/jwt/create/ \
-H "Content-Type: application/json" \
-d '{"username": "ваш_username", "password": "ваш_password"}'
```

Ответ:

```json
{
  "refresh": "ваш_refresh_token",
  "access": "ваш_access_token"
}
```

### Работа с постами

Получение списка постов (пагинация):

```bash
curl -X GET "http://localhost:8000/api/v1/posts/?limit=10&offset=0"
```

Создание нового поста (требуется аутентификация):

```bash
curl -X POST http://localhost:8000/api/v1/posts/ \
-H "Authorization: Bearer ваш_access_token" \
-H "Content-Type: application/json" \
-d '{"text": "Мой первый пост", "group": 1}'
```

### Комментарии

Добавление комментария к посту:

```bash
curl -X POST http://localhost:8000/api/v1/posts/1/comments/ \
-H "Authorization: Bearer ваш_access_token" \
-H "Content-Type: application/json" \
-d '{"text": "Интересный пост!"}'
```

### Подписки

Подписаться на пользователя:

```bash
curl -X POST http://localhost:8000/api/v1/follow/ \
-H "Authorization: Bearer ваш_access_token" \
-H "Content-Type: application/json" \
-d '{"following": "username_автора"}'
```

### Группы

Получение информации о группе:

```bash
curl -X GET http://localhost:8000/api/v1/groups/1/
```

## Документация API

Полная документация доступна по эндпоинтам:

- `/redoc/` - документация в формате ReDoc

- `/swagger/` - интерактивная документация Swagger

## Особенности

- Требуется аутентификация для создания/изменения контента

- Пагинация реализована через параметры `limit` и `offset`

- Поиск по подпискам через параметр `search`

- Валидация данных на стороне сервера

- Обработка ошибок с детальными сообщениями

Для работы с изображениями в постах используйте `multipart/form-data`:
```bash
curl -X POST http://localhost:8000/api/v1/posts/ \
-H "Authorization: Bearer ваш_access_token" \
-F "text=Пост с картинкой" \
-F "image=@/path/to/image.jpg"
```