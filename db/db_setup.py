import os

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")  # PostgreSQL server address
POSTGRES_PORT = os.getenv("POSTGRES_PORT")  # Default PostgreSQL port
POSTGRES_USER = os.getenv("POSTGRES_USER")  # PostgreSQL username
POSTGRES_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD"
)  # PostgreSQL password (default empty)
POSTGRES_DB = os.getenv("POSTGRES_DB")  # PostgreSQL database name

print("POSTGRES_SERVER >>", POSTGRES_SERVER)
print("POSTGRES_PORT >>", POSTGRES_PORT)
print("POSTGRES_USER >>", POSTGRES_USER)
print("POSTGRES_PASSWORD >>", POSTGRES_PASSWORD)
print("POSTGRES_DB >>", POSTGRES_DB)

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


ASYNC_SQLALCHEMY_DATABASE_URL = (
    "postgresql+asyncpg://postgres:postgres@localhost:5442/fastapi_db"
)


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={}, future=True)


async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)


AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def async_get_db():
    async with AsyncSessionLocal() as db:
        yield db
