# Система управления скидками и акциями в супермаркете

## Установка и запуск

### 1. Установи Python 3.11
https://python.org/downloads

### 2. Установи PostgreSQL 15
https://postgresql.org/download/windows
Создай базу данных `promo_db`

### 3. Клонируй репозиторий

git clone https://github.com/dorojill/promo-system.git
cd promo-system

### 4. Создай виртуальное окружение

python -m venv venv
venv\Scripts\activate

### 5. Установи зависимости

pip install -r requirements.txt

### 6. Настрой базу данных
В файле `promo_project/settings.py` укажи пароль от PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'promo_db',
        'USER': 'postgres',
        'PASSWORD': 'твой_пароль',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 7. Примени миграции

python manage.py migrate

### 8. Создай администратора

python manage.py createsuperuser

### 9. Запусти сервер

python manage.py runserver

### Или дважды кликни на `start.bat`

## Открой в браузере
- http://127.0.0.1:8000/ — главная страница
- http://127.0.0.1:8000/admin/ — административная панель
- http://127.0.0.1:8000/promotions/ — список акций
- http://127.0.0.1:8000/calculator/ — калькулятор скидок
- http://127.0.0.1:8000/analytics/ — отчёты

## Технологии
- Python 3.11
- Django 4.2
- PostgreSQL 15
- Bootstrap 5
- Chart.js