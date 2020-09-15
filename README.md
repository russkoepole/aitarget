#  Веб-сервис для библиотеки

## Запуск

* Выполняем `git clone ...`
* Выполняем команду `docker-compose up --build`

## CRUD и права пользователей

* Реализован CRUD для работы со всеми сущностями
* По дефолту (из дата-миграции) создаётся один пользователь (login: `user` / pass: `user000+`) и один администратор (login: `admin` / pass: `admin00+`)
* У Пользователей есть права только на чтение (в рамках endpoint'ов Книг и Авторов)
* Во всех остальных случаях пользователь получит сообщение о недостатке прав для выполнения операций
* Администратор имеет все достпуные ему привелегии, может использовать весь CRUD в рамках работы с любой сущностью
* Доступен поиск по названию книги через `query_params` (`../api/library/books/?title=...`)
* Книги с годом публикации > текущего доступны только администратору
* Настроен smtp-сервер для рассылки сообщений подписчикам о добавлении новой книги

## Маршруты API

### Книги
* `../api/library/books/` (GET, POST)
* `../api/library/books/<book_uuid>/` (GET, PUT, DELETE, PATCH)

### Жанры
* `../api/library/genres/` (GET, POST)
* `../api/library/genres/<genre_id>/` (GET, PUT, DELETE, PATCH)

### Языки
* `../api/library/languages/` (GET, POST)
* `../api/library/languages/<language_id>/` (GET, PUT, DELETE, PATCH)

### Пользователи
* `../api/library/users/` (GET, POST)
* `../api/library/users/<user_uuid>/` (GET, PUT, DELETE, PATCH)

### Авторы
* `../api/library/authors/` (GET, POST)
* `../api/library/authors/<author_uuid>/` (GET, PUT, DELETE, PATCH)

### Подписчики
* `../api/library/followers/` (GET, POST)
* `../api/library/followers/<follower_uuid>/` (GET, PUT, DELETE, PATCH)
