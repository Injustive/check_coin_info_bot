from db.db import insert_or_update, delete_coin, coins_list
from errors import NoCoinsDataError
from utils.emojis import *


async def add_coin_to_db(user_id: int, coin: str) -> str:
    """Добавление монеты в БД. Дополнительная проверка есть ли уже монета в БД"""

    coins = await coins_list(user_id)
    if coins and coin in coins:
        return f'У вас уже есть эта монета!{EMOJI_CROSS_MARK}'
    elif coins and len(coins) >= 10:
        return f"Максимальное число монет - 10. Сначала удалите какую-то монету.{EMOJI_CROSS_MARK}"

    await insert_or_update(user_id, coin)
    return f'Монета {coin.upper()} успешно добавлена!{EMOJI_CHECK_MARK}'


async def check_coins(user_id: int) -> list:
    """Возвращает список монет пользователя, если они есть"""

    coins = await coins_list(user_id)
    if not coins:
        raise NoCoinsDataError

    return coins


async def delete_coin_from_db(user_id: int, coin: str) -> str:
    """Удаление монеты с БД. Дополнительная проверка, есть ли у пользователя список монет"""

    if not await coins_list(user_id):
        raise NoCoinsDataError

    await delete_coin(user_id, coin)
    return f'Монета {coin.upper()} успешно удалена{EMOJI_CHECK_MARK}'
