
# Li2Events

**Li2Events** — это веб-приложение на Flask для управления событиями и пользователями через браузер и REST API. Cобытиями могут, как пример, воприниматься турниры по Майнкрафту, PUBG и т.д.

## 🚀 Описание

Функциональность проекта:
- Регистрация и авторизация пользователей.
- Управление событиями (создание, просмотр).
- Работа с API для интеграции с внешними сервисами.

## 🗂 Структура проекта

| Путь | Описание |
|:-----|:---------|
| `main.py` | Запуск Flask сервера |
| `api/users_api.py` | API для управления пользователями |
| `api/events_api.py` | API для работы с событиями |
| `data/__all_models.py` | Импорты моделей базы данных |
| `data/db_session.py` | Подключение к базе SQLite через SQLAlchemy |
| `form/user.py` | Форма регистрации |
| `form/login.py` | Форма входа |
| `form/profile.py` | Форма редактирования профиля |
| `test.py` | Примеры запросов к API |

## ⚙️ Установка и запуск

1. Клонируйте репозиторий и перейдите в папку проекта:

```bash
git clone https://github.com/your_username/Li2Events.git
cd Li2Events-master
```

2. Создайте виртуальное окружение и активируйте его:

```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux/macOS
venv\Scripts\activate   # Для Windows
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Запустите сервер:

```bash
flask run
```

По умолчанию приложение будет доступно на `http://localhost:5000`

## 📚 API Эндпоинты

### Пользователи
- `GET /api/users` — получить список всех пользователей
- `GET /api/users/<id>` — получить одного пользователя
- `POST /api/users` — создать пользователя

### События
- `GET /api/events` — получить список всех событий
- `GET /api/events/<id>` — получить событие
- `POST /api/events` — создать событие

## 🧩 Используемые технологии

- Python 3.10+
- Flask
- Flask-WTF
- SQLAlchemy
- Requests

## 📈 В разработке

- Добавление JWT-аутентификации для API
- Расширение профилей пользователей
- Фильтрация событий по категориям или датам
- Интерфейс администратора
