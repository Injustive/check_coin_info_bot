import os

import asyncpg
from dotenv import load_dotenv
import socket

from loggers.loggers import db_logger
from utils.db_queries import *

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

POSTGRES_NAME = os.getenv('POSTGRES_NAME')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PSW = os.getenv('POSTGRES_PSW')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')

DSN = f'postgresql://{POSTGRES_USER}:{POSTGRES_PSW}@{POSTGRES_HOST}/{POSTGRES_NAME}'


async def connect_db(user) -> asyncpg.Connection:
    """Функция подключения к БД"""

    try:
        conn = await asyncpg.connect(DSN)
        await conn.execute(CREATE_TABLE_QUERY)
        db_logger.info(f'Пользователь {user} подключился к БД')

        return conn
    except socket.gaierror as err:              # Ошибки связанные с адресами, для getaddrinfo() и getnameinfo()
        db_logger.error(f"Пользователю {user} не удалось подключиться к БД. Причина - {err}")


async def insert_or_update(user_id: int, coin: str) -> None:
    """Вставка или обновление монет в БД"""

    conn = await connect_db(user_id)

    await conn.execute(INSERT_OR_UPDATE_QUERY, user_id, (coin,), coin)
    db_logger.info(f"Пользователь {user_id} добавил монету {coin}")


async def coins_list(user_id) -> list:
    """Возвращает список монет пользователя"""

    conn = await connect_db(user_id)
    data = await conn.fetchval(GET_COINS_LIST_QUERY, user_id)

    return data


async def delete_coin(user_id: int, coin: str) -> None:
    """Удаляет монету по id пользователя"""

    conn = await connect_db(user_id)
    await conn.execute(DELETE_COIN_QUERY, coin, user_id)
    db_logger.info(f"Пользователь {user_id} удалил монету {coin}")





