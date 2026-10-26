
# Импортируем DeclarativeBase для создания базового класса моделей SQLAlchemy,
# а sessionmaker — для создания сессий работы с базой данных.
from sqlalchemy.orm import DeclarativeBase, sessionmaker
# getenv позволяет получать значения переменных окружения.
from os import getenv
# load_dotenv загружает переменные из файла .env.
from dotenv import load_dotenv
# create_engine создаёт объект, через который SQLAlchemy подключается к БД.
from sqlalchemy import create_engine

# Загружаем переменные окружения из файла .env.
load_dotenv()

# Получаем строку подключения к PostgreSQL из переменной DATABASE_URL.
DATABASE_URL = getenv("DATABASE_URL")

# Проверяем, что строка подключения задана.
# Если её нет, останавливаем выполнение и сообщаем о проблеме.
if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL is not set")

# Создаём engine — основной объект SQLAlchemy для взаимодействия с БД.
engine = create_engine(DATABASE_URL)

# Создаём фабрику сессий.
# Через SessionLocal() можно получать отдельные сессии для запросов к БД.
SessionLocal = sessionmaker(bind=engine)

# Функция для предоставления сессии базе данных, например, обработчикам API.
def get_db():
    # Создаём новую сессию.
    db = SessionLocal()
    try:
        # yield передаёт сессию вызывающему коду.
        # После завершения работы выполнение продолжится в блоке finally.
        yield db
    finally:
        # Закрываем сессию, чтобы освободить связанные с ней ресурсы.
        db.close()

# Базовый класс для моделей SQLAlchemy.
# Модели User, Material и другие наследуются от Base.
# SQLAlchemy собирает сведения об их таблицах в Base.metadata.
class Base(DeclarativeBase):
    pass

# проверка подключения пайтон к postgresql
# with engine.connect() as connection:
#     result = connection.execute(text("SELECT 1"))
#     print(result.scalar())