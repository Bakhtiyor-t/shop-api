# Shop-API V1
### Описание проекта
API- для учёта и отчёта расходов, доходов, прибыли и долгов продуктового магазина. [демо]()
### Стек технологий
- FastApi
- JWT Auth
- SQLAlchemy
- Pydantic
- PostgreSQL
- Alembic
- Docker
- Uvicorn
- PyTest

---

### Установка

Убедитесь что у вас установлен python и docker, docker-compose.

```bash
python --version
```

```
docker --version
```

```
docker-compose --version
```

Переходим в рабочую директорию и клонируем проект.
```bash
git clone https://github.com/baxti01/shop-api.git
```
Устанавливаем зависимости.
```
pip install -r requirements.txt
```

Создаём .env файл и добавляем следующие настройки

- Настройки сервера
  - `SERVER_HOST=`... (поумолчанию 0.0.0.0)
  - `SERVER_PORT=`... (поумолчанию 8000)
  - `WORKERS=`... (поумолчанию 1) - количество воркеров uvicorn
- Настройки базы данных 
  - `POSTGRES_HOST=`... (поумолчанию 0.0.0.0)
  - `POSTGRES_PORT=`... (поумолчанию 5432)
  - `POSTGRES_DB=`... (обязательное поле)
  - `POSTGRES_USER=`... (обязательное поле)
  - `POSTGRES_PASSWORD=`... (обязательное поле)
- Настройки JWT Auth
  - `JWT_SECRET=`... (обязательное поле)
  - `JWT_ALGORITHM=`... (обязательное поле)
  - `JWT_EXPIRE_MINUTES=`... (обязательное поле)

Запускаем проект на компьютере

```
python main.py
```

Запускаем проект в docker. Но для этого обязательно укажите **POSTGRES_HOST=db**

```
docker-compose up
```

И пользуемся!

---