# Lesson Schedule Telegram Bot

Бот для получения расписания на сегодня по tg_login (Telegram username).

## Запуск

### Backend (Django API)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # для доступа в админку
python manage.py runserver
```

API: http://127.0.0.1:8000/api/schedule/?tg_login=username

### Bot (aiogram)

```bash
cd bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
BOT_TOKEN=xxx API_URL=http://127.0.0.1:8000 python main.py
# Если порт 8000 занят: API_URL=http://127.0.0.1:8001 python main.py
```

### Переменные окружения

| Переменная | Описание |
|------------|----------|
| BOT_TOKEN | Токен бота от @BotFather |
| API_URL | URL Django API (по умолчанию http://127.0.0.1:8000) |

### Настройка данных

1. Зайти в админку: http://127.0.0.1:8000/admin/
2. Создать группы (1А, 2Б), кабинеты, предметы
3. Добавить уроки (группа, предмет, кабинет, день недели, порядок)
4. Добавить студентов (tg_login — username без @, группа)
