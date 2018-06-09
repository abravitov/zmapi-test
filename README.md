# Внутри папки проекта:

## Установка виртуальной среды 

`python3 -m venv venv`

## Переход в виртуальную среду 

`. venv/bin/activate`

## Установка необходимых дополнений 

`pip install -r requirements.txt`

## Экспорт требуемых переменных для старта приложения

```
export FLASK_ENV=development
export OAUTHLIB_INSECURE_TRANSPORT=1
export FLASK_APP=app.py
```

## Запуск приложения

`flask run`
